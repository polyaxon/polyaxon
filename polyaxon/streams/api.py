import asyncio
import json
import logging

from sanic import Sanic
from websockets import ConnectionClosed

from django.core.exceptions import ValidationError

import auditor

from db.models.build_jobs import BuildJob
from db.models.experiment_jobs import ExperimentJob
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.projects import Project
from event_manager.events.build_job import BUILD_JOB_LOGS_VIEWED
from event_manager.events.experiment import EXPERIMENT_LOGS_VIEWED, EXPERIMENT_RESOURCES_VIEWED
from event_manager.events.experiment_job import (
    EXPERIMENT_JOB_LOGS_VIEWED,
    EXPERIMENT_JOB_RESOURCES_VIEWED
)
from event_manager.events.job import JOB_LOGS_VIEWED
from libs.permissions.projects import has_project_permissions
from libs.redis_db import RedisToStream
from polyaxon.settings import CeleryQueues, RoutingKeys
from streams.authentication import authorized
from streams.consumers import Consumer
from streams.socket_manager import SocketManager

_logger = logging.getLogger('polyaxon.streams.api')

SOCKET_SLEEP = 2
MAX_RETRIES = 7
RESOURCES_CHECK = 7
CHECK_DELAY = 5

app = Sanic(__name__)


def get_error_message(message):
    return json.dumps({'status': 'error', 'log_lines': [message]})


def validate_project(request, username, project_name):
    try:
        project = Project.objects.get(name=project_name, user__username=username)
    except Project.DoesNotExist:
        return None, 'Project was not found'
    if not has_project_permissions(request.app.user, project, 'GET'):
        return None, "You don't have access to this project"
    return project, None


def validate_experiment(request, username, project_name, experiment_id):
    project, message = validate_project(request=request,
                                        username=username,
                                        project_name=project_name)
    if project is None:
        return None, message
    try:
        experiment = Experiment.objects.get(project=project, id=experiment_id)
    except (Experiment.DoesNotExist, ValidationError):
        return None, 'Experiment was not found'
    if not experiment.is_running:
        return None, 'Experiment was not running'
    return experiment, None


def validate_experiment_job(request, username, project_name, experiment_id, job_id):
    experiment, message = validate_experiment(request=request,
                                              username=username,
                                              project_name=project_name,
                                              experiment_id=experiment_id)
    if experiment is None:
        return None, None, message
    try:
        job = ExperimentJob.objects.get(experiment=experiment, id=job_id)
    except (ExperimentJob.DoesNotExist, ValidationError):
        return None, None, 'Experiment was not found'
    if not job.is_running:
        return None, None, 'Job was not running'
    return job, experiment, None


def validate_job(request, username, project_name, job_id):
    project, message = validate_project(request=request,
                                        username=username,
                                        project_name=project_name)
    if project is None:
        return None, message
    try:
        job = Job.objects.get(project=project, id=job_id)
    except (Experiment.DoesNotExist, ValidationError):
        return None, 'Job was not found'
    if not job.is_running:
        return None, 'Job was not running'
    return job, None


def validate_build(request, username, project_name, build_id):
    project, message = validate_project(request=request,
                                        username=username,
                                        project_name=project_name)
    if project is None:
        return None, message
    try:
        job = BuildJob.objects.get(project=project, id=build_id)
    except (Experiment.DoesNotExist, ValidationError):
        return None, 'Build was not found'
    if not job.is_running:
        return None, 'Build was not running'
    return job, None


@authorized()
async def experiment_job_resources(request, ws, username, project_name, experiment_id, job_id):
    job, _, message = validate_experiment_job(request=request,
                                              username=username,
                                              project_name=project_name,
                                              experiment_id=experiment_id,
                                              job_id=job_id)
    if job is None:
        await ws.send(get_error_message(message))
        return
    job_uuid = job.uuid.hex
    job_name = '{}.{}'.format(job.role, job.id)
    auditor.record(event_type=EXPERIMENT_JOB_RESOURCES_VIEWED,
                   instance=job,
                   actor_id=request.app.user.id)

    if not RedisToStream.is_monitored_job_resources(job_uuid=job_uuid):
        _logger.info('Job resources with uuid `%s` is now being monitored', job_name)
        RedisToStream.monitor_job_resources(job_uuid=job_uuid)

    if job_uuid in request.app.job_resources_ws_mangers:
        ws_manager = request.app.job_resources_ws_mangers[job_uuid]
    else:
        ws_manager = SocketManager()
        request.app.job_resources_ws_mangers[job_uuid] = ws_manager

    def handle_job_disconnected_ws(ws):
        ws_manager.remove_sockets(ws)
        if not ws_manager.ws:
            _logger.info('Stopping resources monitor for job %s', job_name)
            RedisToStream.remove_job_resources(job_uuid=job_uuid)
            request.app.job_resources_ws_mangers.pop(job_uuid, None)

        _logger.info('Quitting resources socket for job %s', job_name)

    ws_manager.add_socket(ws)
    should_check = 0
    while True:
        resources = RedisToStream.get_latest_job_resources(job=job_uuid, job_name=job_name)
        should_check += 1

        # After trying a couple of time, we must check the status of the job
        if should_check > RESOURCES_CHECK:
            job.refresh_from_db()
            if job.is_done:
                _logger.info('removing all socket because the job `%s` is done', job_name)
                ws_manager.ws = set([])
                handle_job_disconnected_ws(ws)
                return
            else:
                should_check -= CHECK_DELAY

        if resources:
            try:
                await ws.send(resources)
            except ConnectionClosed:
                handle_job_disconnected_ws(ws)
                return

        # Just to check if connection closed
        if ws._connection_lost:  # pylint:disable=protected-access
            handle_job_disconnected_ws(ws)
            return
        await asyncio.sleep(SOCKET_SLEEP)


@authorized()
async def experiment_resources(request, ws, username, project_name, experiment_id):
    experiment, message = validate_experiment(request=request,
                                              username=username,
                                              project_name=project_name,
                                              experiment_id=experiment_id)
    if experiment is None:
        await ws.send(get_error_message(message))
        return
    experiment_uuid = experiment.uuid.hex
    auditor.record(event_type=EXPERIMENT_RESOURCES_VIEWED,
                   instance=experiment,
                   actor_id=request.app.user.id)

    if not RedisToStream.is_monitored_experiment_resources(experiment_uuid=experiment_uuid):
        _logger.info('Experiment resource with uuid `%s` is now being monitored', experiment_uuid)
        RedisToStream.monitor_experiment_resources(experiment_uuid=experiment_uuid)

    if experiment_uuid in request.app.experiment_resources_ws_mangers:
        ws_manager = request.app.experiment_resources_ws_mangers[experiment_uuid]
    else:
        ws_manager = SocketManager()
        request.app.experiment_resources_ws_mangers[experiment_uuid] = ws_manager

    def handle_experiment_disconnected_ws(ws):
        ws_manager.remove_sockets(ws)
        if not ws_manager.ws:
            _logger.info('Stopping resources monitor for uuid %s', experiment_uuid)
            RedisToStream.remove_experiment_resources(experiment_uuid=experiment_uuid)
            request.app.experiment_resources_ws_mangers.pop(experiment_uuid, None)

        _logger.info('Quitting resources socket for uuid %s', experiment_uuid)

    jobs = []
    for job in experiment.jobs.values('uuid', 'role', 'id'):
        job['uuid'] = job['uuid'].hex
        job['name'] = '{}.{}'.format(job.pop('role'), job.pop('id'))
        jobs.append(job)
    ws_manager.add_socket(ws)
    should_check = 0
    while True:
        resources = RedisToStream.get_latest_experiment_resources(jobs)
        should_check += 1

        # After trying a couple of time, we must check the status of the experiment
        if should_check > RESOURCES_CHECK:
            experiment.refresh_from_db()
            if experiment.is_done:
                _logger.info(
                    'removing all socket because the experiment `%s` is done', experiment_uuid)
                ws_manager.ws = set([])
                handle_experiment_disconnected_ws(ws)
                return
            else:
                should_check -= CHECK_DELAY

        if resources:
            try:
                await ws.send(resources)
            except ConnectionClosed:
                handle_experiment_disconnected_ws(ws)
                return

        # Just to check if connection closed
        if ws._connection_lost:  # pylint:disable=protected-access
            handle_experiment_disconnected_ws(ws)
            return

        await asyncio.sleep(SOCKET_SLEEP)


@authorized()
async def experiment_job_logs(request, ws, username, project_name, experiment_id, job_id):
    job, experiment, message = validate_experiment_job(request=request,
                                                       username=username,
                                                       project_name=project_name,
                                                       experiment_id=experiment_id,
                                                       job_id=job_id)
    if job is None:
        await ws.send(get_error_message(message))
        return
    job_uuid = job.uuid.hex
    auditor.record(event_type=EXPERIMENT_JOB_LOGS_VIEWED,
                   instance=job,
                   actor_id=request.app.user.id)

    if not RedisToStream.is_monitored_job_logs(job_uuid=job_uuid):
        _logger.info('Job uuid `%s` logs is now being monitored', job_uuid)
        RedisToStream.monitor_job_logs(job_uuid=job_uuid)

    # start consumer
    if job_uuid in request.app.job_logs_consumers:
        consumer = request.app.job_logs_consumers[job_uuid]
    else:
        _logger.info('Add job log consumer for %s', job_uuid)
        consumer = Consumer(
            routing_key='{}.{}.{}'.format(RoutingKeys.LOGS_SIDECARS_EXPERIMENTS,
                                          experiment.uuid.hex,
                                          job_uuid),
            queue='{}.{}'.format(CeleryQueues.STREAM_LOGS_SIDECARS, job_uuid))
        request.app.job_logs_consumers[job_uuid] = consumer
        consumer.run()

    # add socket manager
    consumer.add_socket(ws)
    should_quite = False
    num_message_retries = 0
    while True:
        num_message_retries += 1
        for message in consumer.get_messages():
            num_message_retries = 0
            disconnected_ws = set()
            for _ws in consumer.ws:
                try:
                    await _ws.send(message)
                except ConnectionClosed:
                    disconnected_ws.add(_ws)
            consumer.remove_sockets(disconnected_ws)

        # After trying a couple of time, we must check the status of the experiment
        if num_message_retries > MAX_RETRIES:
            job.refresh_from_db()
            if job.is_done:
                _logger.info('removing all socket because the job `%s` is done', job_uuid)
                consumer.ws = set([])
            else:
                num_message_retries -= CHECK_DELAY

        # Just to check if connection closed
        if ws._connection_lost:  # pylint:disable=protected-access
            _logger.info('Quitting logs socket for job uuid %s', job_uuid)
            consumer.remove_sockets({ws, })
            should_quite = True

        if not consumer.ws:
            _logger.info('Stopping logs monitor for job uuid %s', job_uuid)
            RedisToStream.remove_job_logs(job_uuid=job_uuid)
            # if job_uuid in request.app.job_logs_consumers:
            #     consumer = request.app.job_logs_consumers.pop(job_uuid, None)
            #     if consumer:
            #         consumer.stop()
            should_quite = True

        if should_quite:
            return

        await asyncio.sleep(SOCKET_SLEEP)


@authorized()
async def experiment_logs(request, ws, username, project_name, experiment_id):
    experiment, message = validate_experiment(request=request,
                                              username=username,
                                              project_name=project_name,
                                              experiment_id=experiment_id)
    if experiment is None:
        await ws.send(get_error_message(message))
        return

    experiment_uuid = experiment.uuid.hex
    auditor.record(event_type=EXPERIMENT_LOGS_VIEWED,
                   instance=experiment,
                   actor_id=request.app.user.id)

    if not RedisToStream.is_monitored_experiment_logs(experiment_uuid=experiment_uuid):
        _logger.info('Experiment uuid `%s` logs is now being monitored', experiment_uuid)
        RedisToStream.monitor_experiment_logs(experiment_uuid=experiment_uuid)

    # start consumer
    if experiment_uuid in request.app.experiment_logs_consumers:
        consumer = request.app.experiment_logs_consumers[experiment_uuid]
    else:
        _logger.info('Add experiment log consumer for %s', experiment_uuid)
        consumer = Consumer(
            routing_key='{}.{}.*'.format(RoutingKeys.LOGS_SIDECARS_EXPERIMENTS, experiment_uuid),
            queue='{}.{}'.format(CeleryQueues.STREAM_LOGS_SIDECARS, experiment_uuid))
        request.app.experiment_logs_consumers[experiment_uuid] = consumer
        consumer.run()

    # add socket manager
    consumer.add_socket(ws)
    should_quite = False
    num_message_retries = 0
    while True:
        num_message_retries += 1
        for message in consumer.get_messages():
            num_message_retries = 0
            disconnected_ws = set()
            for _ws in consumer.ws:
                try:
                    await _ws.send(message)
                except ConnectionClosed:
                    disconnected_ws.add(_ws)
            consumer.remove_sockets(disconnected_ws)

        # After trying a couple of time, we must check the status of the experiment
        if num_message_retries > MAX_RETRIES:
            experiment.refresh_from_db()
            if experiment.is_done:
                _logger.info(
                    'removing all socket because the experiment `%s` is done', experiment_uuid)
                consumer.ws = set([])
            else:
                num_message_retries -= CHECK_DELAY

        # Just to check if connection closed
        if ws._connection_lost:  # pylint:disable=protected-access
            _logger.info('Quitting logs socket for experiment uuid %s', experiment_uuid)
            consumer.remove_sockets({ws, })
            should_quite = True

        if not consumer.ws:
            _logger.info('Stopping logs monitor for experiment uuid %s', experiment_uuid)
            RedisToStream.remove_experiment_logs(experiment_uuid=experiment_uuid)
            # if experiment_uuid in request.app.experiment_logs_consumers:
            #     consumer = request.app.experiment_logs_consumers.pop(experiment_uuid, None)
            #     if consumer:
            #         consumer.stop()
            should_quite = True

        if should_quite:
            return

        await asyncio.sleep(SOCKET_SLEEP)


@authorized()
async def job_logs(request, ws, username, project_name, job_id):
    job, message = validate_job(request=request,
                                username=username,
                                project_name=project_name,
                                job_id=job_id)
    if job is None:
        await ws.send(get_error_message(message))
        return
    job_uuid = job.uuid.hex
    auditor.record(event_type=JOB_LOGS_VIEWED,
                   instance=job,
                   actor_id=request.app.user.id)

    if not RedisToStream.is_monitored_job_logs(job_uuid=job_uuid):
        _logger.info('Job uuid `%s` logs is now being monitored', job_uuid)
        RedisToStream.monitor_job_logs(job_uuid=job_uuid)

    # start consumer
    if job_uuid in request.app.job_logs_consumers:
        consumer = request.app.job_logs_consumers[job_uuid]
    else:
        _logger.info('Add job log consumer for %s', job_uuid)
        consumer = Consumer(
            routing_key='{}.{}'.format(RoutingKeys.LOGS_SIDECARS_JOBS, job_uuid),
            queue='{}.{}'.format(CeleryQueues.STREAM_LOGS_SIDECARS, job_uuid))
        request.app.job_logs_consumers[job_uuid] = consumer
        consumer.run()

    # add socket manager
    consumer.add_socket(ws)
    should_quite = False
    num_message_retries = 0
    while True:
        num_message_retries += 1
        for message in consumer.get_messages():
            num_message_retries = 0
            disconnected_ws = set()
            for _ws in consumer.ws:
                try:
                    await _ws.send(message)
                except ConnectionClosed:
                    disconnected_ws.add(_ws)
            consumer.remove_sockets(disconnected_ws)

        # After trying a couple of time, we must check the status of the experiment
        if num_message_retries > MAX_RETRIES:
            job.refresh_from_db()
            if job.is_done:
                _logger.info('removing all socket because the job `%s` is done', job_uuid)
                consumer.ws = set([])
            else:
                num_message_retries -= CHECK_DELAY

        # Just to check if connection closed
        if ws._connection_lost:  # pylint:disable=protected-access
            _logger.info('Quitting logs socket for job uuid %s', job_uuid)
            consumer.remove_sockets({ws, })
            should_quite = True

        if not consumer.ws:
            _logger.info('Stopping logs monitor for job uuid %s', job_uuid)
            RedisToStream.remove_job_logs(job_uuid=job_uuid)
            # if job_uuid in request.app.job_logs_consumers:
            #     consumer = request.app.job_logs_consumers.pop(job_uuid, None)
            #     if consumer:
            #         consumer.stop()
            should_quite = True

        if should_quite:
            return

        await asyncio.sleep(SOCKET_SLEEP)


@authorized()
async def build_logs(request, ws, username, project_name, build_id):
    job, message = validate_build(request=request,
                                  username=username,
                                  project_name=project_name,
                                  build_id=build_id)
    if job is None:
        await ws.send(get_error_message(message))
        return
    job_uuid = job.uuid.hex
    auditor.record(event_type=BUILD_JOB_LOGS_VIEWED,
                   instance=job,
                   actor_id=request.app.user.id)

    if not RedisToStream.is_monitored_job_logs(job_uuid=job_uuid):
        _logger.info('Job uuid `%s` logs is now being monitored', job_uuid)
        RedisToStream.monitor_job_logs(job_uuid=job_uuid)

    # start consumer
    if job_uuid in request.app.job_logs_consumers:
        consumer = request.app.job_logs_consumers[job_uuid]
    else:
        _logger.info('Add job log consumer for %s', job_uuid)
        consumer = Consumer(
            routing_key='{}.{}'.format(RoutingKeys.LOGS_SIDECARS_JOBS, job_uuid),
            queue='{}.{}'.format(CeleryQueues.STREAM_LOGS_SIDECARS, job_uuid))
        request.app.job_logs_consumers[job_uuid] = consumer
        consumer.run()

    # add socket manager
    consumer.add_socket(ws)
    should_quite = False
    num_message_retries = 0
    while True:
        num_message_retries += 1
        for message in consumer.get_messages():
            num_message_retries = 0
            disconnected_ws = set()
            for _ws in consumer.ws:
                try:
                    await _ws.send(message)
                except ConnectionClosed:
                    disconnected_ws.add(_ws)
            consumer.remove_sockets(disconnected_ws)

        # After trying a couple of time, we must check the status of the experiment
        if num_message_retries > MAX_RETRIES:
            job.refresh_from_db()
            if job.is_done:
                _logger.info('removing all socket because the job `%s` is done', job_uuid)
                consumer.ws = set([])
            else:
                num_message_retries -= CHECK_DELAY

        # Just to check if connection closed
        if ws._connection_lost:  # pylint:disable=protected-access
            _logger.info('Quitting logs socket for job uuid %s', job_uuid)
            consumer.remove_sockets({ws, })
            should_quite = True

        if not consumer.ws:
            _logger.info('Stopping logs monitor for job uuid %s', job_uuid)
            RedisToStream.remove_job_logs(job_uuid=job_uuid)
            # if job_uuid in request.app.job_logs_consumers:
            #     consumer = request.app.job_logs_consumers.pop(job_uuid, None)
            #     if consumer:
            #         consumer.stop()
            should_quite = True

        if should_quite:
            return

        await asyncio.sleep(SOCKET_SLEEP)


EXPERIMENT_URL = '/v1/<username>/<project_name>/experiments/<experiment_id>'
BUILD_URL = '/v1/<username>/<project_name>/builds/<build_id>'
JOB_URL = '/v1/<username>/<project_name>/jobs/<job_id>'


def add_url(endpoint, base_url, url):
    app.add_websocket_route(endpoint, '{}/{}'.format(base_url, url))
    app.add_websocket_route(endpoint, '/ws{}/{}'.format(base_url, url))


# Experiment Job urls
add_url(endpoint=experiment_job_resources, base_url=EXPERIMENT_URL, url='jobs/<job_id>/resources')
add_url(endpoint=experiment_job_logs, base_url=EXPERIMENT_URL, url='jobs/<job_id>/logs')

# Experiment urls
add_url(endpoint=experiment_resources, base_url=EXPERIMENT_URL, url='resources')
add_url(endpoint=experiment_logs, base_url=EXPERIMENT_URL, url='logs')

# Job urls
# add_url(endpoint=job_resources, base_url=EXPERIMENT_URL, url='resources')
add_url(endpoint=job_logs, base_url=JOB_URL, url='logs')

# Build Job urls
# add_url(endpoint=job_resources, base_url=EXPERIMENT_URL, url='resources')
add_url(endpoint=build_logs, base_url=BUILD_URL, url='logs')


@app.listener('after_server_start')
async def notify_server_started(app, loop):  # pylint:disable=redefined-outer-name
    app.job_resources_ws_mangers = {}
    app.experiment_resources_ws_mangers = {}
    app.job_logs_consumers = {}
    app.experiment_logs_consumers = {}


@app.listener('after_server_stop')
async def notify_server_stopped(app, loop):  # pylint:disable=redefined-outer-name
    app.job_resources_ws_mangers = {}
    app.experiment_resources_ws_manger = {}

    consumer_keys = list(app.job_logs_consumers.keys())
    for consumer_key in consumer_keys:
        consumer = app.job_logs_consumers.pop(consumer_key, None)
        consumer.stop()

    consumer_keys = list(app.experiment_logs_consumers.keys())
    for consumer_key in consumer_keys:
        consumer = app.experiment_logs_consumers.pop(consumer_key, None)
        consumer.stop()
