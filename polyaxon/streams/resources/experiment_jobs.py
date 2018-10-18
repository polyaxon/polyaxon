import asyncio

from websockets import ConnectionClosed

import auditor
from db.redis.to_stream import RedisToStream
from event_manager.events.experiment_job import (
    EXPERIMENT_JOB_RESOURCES_VIEWED,
    EXPERIMENT_JOB_LOGS_VIEWED
)
from polyaxon.settings import CeleryQueues, RoutingKeys
from streams.authentication import authorized
from streams.constants import RESOURCES_CHECK, CHECK_DELAY, SOCKET_SLEEP, MAX_RETRIES
from streams.consumers import Consumer
from streams.logger import logger
from streams.resources.utils import get_error_message, notify
from streams.socket_manager import SocketManager
from streams.validation.experiment_job import validate_experiment_job


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
                   actor_id=request.app.user.id,
                   actor_name=request.app.user.username)

    if not RedisToStream.is_monitored_job_resources(job_uuid=job_uuid):
        logger.info('Job resources with uuid `%s` is now being monitored', job_name)
        RedisToStream.monitor_job_resources(job_uuid=job_uuid)

    if job_uuid in request.app.job_resources_ws_mangers:
        ws_manager = request.app.job_resources_ws_mangers[job_uuid]
    else:
        ws_manager = SocketManager()
        request.app.job_resources_ws_mangers[job_uuid] = ws_manager

    def handle_job_disconnected_ws(ws):
        ws_manager.remove_sockets(ws)
        if not ws_manager.ws:
            logger.info('Stopping resources monitor for job %s', job_name)
            RedisToStream.remove_job_resources(job_uuid=job_uuid)
            request.app.job_resources_ws_mangers.pop(job_uuid, None)

        logger.info('Quitting resources socket for job %s', job_name)

    ws_manager.add_socket(ws)
    should_check = 0
    while True:
        resources = RedisToStream.get_latest_job_resources(job=job_uuid, job_name=job_name)
        should_check += 1

        # After trying a couple of time, we must check the status of the job
        if should_check > RESOURCES_CHECK:
            job.refresh_from_db()
            if job.is_done:
                logger.info('removing all socket because the job `%s` is done', job_name)
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
                   actor_id=request.app.user.id,
                   actor_name=request.app.user.username)

    if not RedisToStream.is_monitored_job_logs(job_uuid=job_uuid):
        logger.info('Job uuid `%s` logs is now being monitored', job_uuid)
        RedisToStream.monitor_job_logs(job_uuid=job_uuid)

    # start consumer
    if job_uuid in request.app.job_logs_consumers:
        consumer = request.app.job_logs_consumers[job_uuid]
    else:
        logger.info('Add job log consumer for %s', job_uuid)
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
            await notify(consumer=consumer, message=message)

        # After trying a couple of time, we must check the status of the experiment
        if num_message_retries > MAX_RETRIES:
            job.refresh_from_db()
            if job.is_done:
                logger.info('removing all socket because the job `%s` is done', job_uuid)
                consumer.ws = set([])
            else:
                num_message_retries -= CHECK_DELAY

        # Just to check if connection closed
        if ws._connection_lost:  # pylint:disable=protected-access
            logger.info('Quitting logs socket for job uuid %s', job_uuid)
            consumer.remove_sockets({ws, })
            should_quite = True

        if not consumer.ws:
            logger.info('Stopping logs monitor for job uuid %s', job_uuid)
            RedisToStream.remove_job_logs(job_uuid=job_uuid)
            # if job_uuid in request.app.job_logs_consumers:
            #     consumer = request.app.job_logs_consumers.pop(job_uuid, None)
            #     if consumer:
            #         consumer.stop()
            should_quite = True

        if should_quite:
            return

        await asyncio.sleep(SOCKET_SLEEP)
