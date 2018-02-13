# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import asyncio
import logging

from django.core.exceptions import ValidationError

from sanic import Sanic
from sanic import exceptions

from websockets import ConnectionClosed

from polyaxon.config_settings.celery_settings import RoutingKeys, CeleryQueues
from events.authentication import authorized
from events.consumers import Consumer
from events.socket_manager import SocketManager
from experiments.models import ExperimentJob, Experiment
from libs.redis_db import RedisToStream
from projects.models import Project
from projects.permissions import has_project_permissions

logger = logging.getLogger('polyaxon.monitors.api')

SOCKET_SLEEP = 1
MAX_RETRIES = 15
RESOURCES_CHECK = 15
CHECK_DELAY = 5

app = Sanic(__name__)


def _get_project(username, project_name):
    try:
        return Project.objects.get(name=project_name, user__username=username)
    except Project.DoesNotExist:
        raise exceptions.NotFound('Project was not found')


def _get_experiment(project, experiment_sequence):
    try:
        return Experiment.objects.get(project=project, sequence=experiment_sequence)
    except (Experiment.DoesNotExist, ValidationError):
        raise exceptions.NotFound('Experiment was not found')


def _get_job(experiment, job_sequence):
    try:
        job = ExperimentJob.objects.get(experiment=experiment, sequence=job_sequence)
    except (ExperimentJob.DoesNotExist, ValidationError):
        logger.info('Job with experiment:`{}` sequence:`{}` does not exist'.format(
            experiment.unique_name, job_sequence))
        raise exceptions.NotFound('Experiment was not found')

    if not job.is_running:
        logger.info('Job with experiment:`{}` sequence:`{}` is not currently running'.format(
            experiment.unique_name, job_sequence))
        raise exceptions.NotFound('Job was not running')

    return job


def _get_validated_experiment(project, experiment_sequence):
    experiment = _get_experiment(project, experiment_sequence)
    if not experiment.is_running:
        logger.info('Experiment project `{}` num `{}` is not currently running'.format(
            project.name, experiment.sequence
        ))
        raise exceptions.NotFound('Experiment was not running')

    return experiment


@authorized()
async def job_resources(request, ws, username, project_name, experiment_sequence, job_sequence):
    project = _get_project(username, project_name)
    if not has_project_permissions(request.app.user, project, 'GET'):
        exceptions.Forbidden("You don't have access to this project")
    experiment = _get_validated_experiment(project, experiment_sequence)
    job = _get_job(experiment, job_sequence)
    job_uuid = job.uuid.hex
    job_name = '{}.{}'.format(job.role, job.sequence)

    if not RedisToStream.is_monitored_job_resources(job_uuid=job_uuid):
        logger.info(
            'Job resources with uuid `{}` is now being monitored'.format(job_name))
        RedisToStream.monitor_job_resources(job_uuid=job_uuid)

    if job_uuid in request.app.job_resources_ws_mangers:
        ws_manager = request.app.job_resources_ws_mangers[job_uuid]
    else:
        ws_manager = SocketManager()
        request.app.job_resources_ws_mangers[job_uuid] = ws_manager

    def handle_job_disconnected_ws(ws):
        ws_manager.remove_sockets(ws)
        if len(ws_manager.ws) == 0:
            logger.info('Stopping resources monitor for job {}'.format(job_name))
            RedisToStream.remove_job_resources(job_uuid=job_uuid)
            request.app.job_resources_ws_mangers.pop(job_uuid, None)

        logger.info('Quitting resources socket for job {}'.format(job_name))

    ws_manager.add_socket(ws)
    should_check = 0
    while True:
        resources = RedisToStream.get_latest_job_resources(job=job_uuid, job_name=job_name)
        should_check += 1

        # After trying a couple of time, we must check the status of the job
        if should_check > RESOURCES_CHECK:
            job.refresh_from_db()
            if job.is_done:
                logger.info('removing all socket because the job `{}` is done'.format(job_name))
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
        if ws._connection_lost:
            handle_job_disconnected_ws(ws)
            return
        await asyncio.sleep(SOCKET_SLEEP)


@authorized()
async def experiment_resources(request, ws, username, project_name, experiment_sequence):
    project = _get_project(username, project_name)
    if not has_project_permissions(request.app.user, project, 'GET'):
        exceptions.Forbidden("You don't have access to this project")
    experiment = _get_validated_experiment(project, experiment_sequence)
    experiment_uuid = experiment.uuid.hex

    if not RedisToStream.is_monitored_experiment_resources(experiment_uuid=experiment_uuid):
        logger.info(
            'Experiment resource with uuid `{}` is now being monitored'.format(experiment_uuid))
        RedisToStream.monitor_experiment_resources(experiment_uuid=experiment_uuid)

    if experiment_uuid in request.app.experiment_resources_ws_mangers:
        ws_manager = request.app.experiment_resources_ws_mangers[experiment_uuid]
    else:
        ws_manager = SocketManager()
        request.app.experiment_resources_ws_mangers[experiment_uuid] = ws_manager

    def handle_experiment_disconnected_ws(ws):
        ws_manager.remove_sockets(ws)
        if len(ws_manager.ws) == 0:
            logger.info('Stopping resources monitor for uuid {}'.format(experiment_uuid))
            RedisToStream.remove_experiment_resources(experiment_uuid=experiment_uuid)
            request.app.experiment_resources_ws_mangers.pop(experiment_uuid, None)

        logger.info('Quitting resources socket for uuid {}'.format(experiment_uuid))

    jobs = []
    for job in experiment.jobs.values('uuid', 'role', 'sequence'):
        job['uuid'] = job['uuid'].hex
        job['name'] = '{}.{}'.format(job.pop('role'), job.pop('sequence'))
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
                logger.info('removing all socket because the experiment `{}` is done'.format(
                    experiment_uuid))
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
        if ws._connection_lost:
            handle_experiment_disconnected_ws(ws)
            return

        await asyncio.sleep(SOCKET_SLEEP)


@authorized()
async def job_logs(request, ws, username, project_name, experiment_sequence, job_sequence):
    project = _get_project(username, project_name)
    if not has_project_permissions(request.app.user, project, 'GET'):
        exceptions.Forbidden("You don't have access to this project")
    experiment = _get_validated_experiment(project, experiment_sequence)
    job = _get_job(experiment, job_sequence)
    job_uuid = job.uuid.hex

    if not RedisToStream.is_monitored_job_logs(job_uuid=job_uuid):
        logger.info('Job uuid `{}` logs is now being monitored'.format(job_uuid))
        RedisToStream.monitor_job_logs(job_uuid=job_uuid)

    # start consumer
    if job_uuid in request.app.job_logs_consumers:
        consumer = request.app.job_logs_consumers[job_uuid]
    else:
        logger.info('Add job log consumer for {}'.format(job_uuid))
        consumer = Consumer(
            routing_key='{}.{}.{}'.format(RoutingKeys.LOGS_SIDECARS,
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
                logger.info('removing all socket because the job `{}` is done'.format(
                    job_uuid))
                consumer.ws = set([])
            else:
                num_message_retries -= CHECK_DELAY

        # Just to check if connection closed
        if ws._connection_lost:
            logger.info('Quitting logs socket for job uuid {}'.format(job_uuid))
            consumer.remove_sockets({ws, })
            should_quite = True

        if len(consumer.ws) == 0:
            logger.info('Stopping logs monitor for job uuid {}'.format(job_uuid))
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
async def experiment_logs(request, ws, username, project_name, experiment_sequence):
    project = _get_project(username, project_name)
    if not has_project_permissions(request.app.user, project, 'GET'):
        exceptions.Forbidden("You don't have access to this project")
    experiment = _get_validated_experiment(project, experiment_sequence)
    experiment_uuid = experiment.uuid.hex

    if not RedisToStream.is_monitored_experiment_logs(experiment_uuid=experiment_uuid):
        logger.info('Experiment uuid `{}` logs is now being monitored'.format(experiment_uuid))
        RedisToStream.monitor_experiment_logs(experiment_uuid=experiment_uuid)

    # start consumer
    if experiment_uuid in request.app.experiment_logs_consumers:
        consumer = request.app.experiment_logs_consumers[experiment_uuid]
    else:
        logger.info('Add experiment log consumer for {}'.format(experiment_uuid))
        consumer = Consumer(
            routing_key='{}.{}.*'.format(RoutingKeys.LOGS_SIDECARS, experiment_uuid),
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
                logger.info('removing all socket because the experiment `{}` is done'.format(
                    experiment_uuid))
                consumer.ws = set([])
            else:
                num_message_retries -= CHECK_DELAY

        # Just to check if connection closed
        if ws._connection_lost:
            logger.info('Quitting logs socket for experiment uuid {}'.format(experiment_uuid))
            consumer.remove_sockets({ws, })
            should_quite = True

        if len(consumer.ws) == 0:
            logger.info('Stopping logs monitor for experiment uuid {}'.format(experiment_uuid))
            RedisToStream.remove_experiment_logs(experiment_uuid=experiment_uuid)
            # if experiment_uuid in request.app.experiment_logs_consumers:
            #     consumer = request.app.experiment_logs_consumers.pop(experiment_uuid, None)
            #     if consumer:
            #         consumer.stop()
            should_quite = True

        if should_quite:
            return

        await asyncio.sleep(SOCKET_SLEEP)


# Job urls
app.add_websocket_route(
    job_resources,
    '/v1/<username>/<project_name>/experiments/<experiment_sequence>/jobs/<job_sequence>/resources')
app.add_websocket_route(
    job_resources,
    '/ws/v1/<username>/<project_name>/experiments/<experiment_sequence>/jobs/<job_sequence>/resources')

app.add_websocket_route(
    job_logs,
    '/v1/<username>/<project_name>/experiments/<experiment_sequence>/jobs/<job_sequence>/logs')
app.add_websocket_route(
    job_logs,
    '/ws/v1/<username>/<project_name>/experiments/<experiment_sequence>/jobs/<job_sequence>/logs')


# Experiment urls
app.add_websocket_route(
    experiment_resources,
    '/v1/<username>/<project_name>/experiments/<experiment_sequence>/resources')
app.add_websocket_route(
    experiment_resources,
    '/ws/v1/<username>/<project_name>/experiments/<experiment_sequence>/resources')

app.add_websocket_route(
    experiment_logs,
    '/v1/<username>/<project_name>/experiments/<experiment_sequence>/logs')
app.add_websocket_route(
    experiment_logs,
    '/ws/v1/<username>/<project_name>/experiments/<experiment_sequence>/logs')


@app.listener('after_server_start')
async def notify_server_started(app, loop):
    app.job_resources_ws_mangers = {}
    app.experiment_resources_ws_mangers = {}
    app.job_logs_consumers = {}
    app.experiment_logs_consumers = {}


@app.listener('after_server_stop')
async def notify_server_stopped(app, loop):
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
