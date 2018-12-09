import asyncio

import auditor

from constants.jobs import JobLifeCycle
from constants.k8s_jobs import JOB_NAME_FORMAT, DOCKERIZER_JOB_NAME
from db.redis.to_stream import RedisToStream
from event_manager.events.build_job import BUILD_JOB_LOGS_VIEWED
from logs_handlers.log_queries.build_job import stream_logs
from polyaxon.settings import CeleryQueues, RoutingKeys
from streams.authentication import authorized
from streams.constants import CHECK_DELAY, MAX_RETRIES, SOCKET_SLEEP
from streams.consumers import Consumer
from streams.logger import logger
from streams.resources.utils import get_error_message, get_status_message, notify
from streams.socket_manager import SocketManager
from streams.validation.build import validate_build


@authorized()
async def build_logs(request,  # pylint:disable=too-many-branches
                     ws,
                     username,
                     project_name,
                     build_id):
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
            routing_key='{}.{}'.format(RoutingKeys.STREAM_LOGS_SIDECARS_BUILDS, job_uuid),
            queue='{}.{}'.format(CeleryQueues.STREAM_LOGS_SIDECARS, job_uuid))
        request.app.job_logs_consumers[job_uuid] = consumer
        consumer.run()

    def should_disconnect():
        if not consumer.ws:
            logger.info('Stopping logs monitor for job uuid %s', job_uuid)
            RedisToStream.remove_job_logs(job_uuid=job_uuid)
            # if job_uuid in request.app.job_logs_consumers:
            #     consumer = request.app.job_logs_consumers.pop(job_uuid, None)
            #     if consumer:
            #         consumer.stop()
            return True
        return False

    # add socket manager
    consumer.add_socket(ws)
    should_quite = False
    num_message_retries = 0

    # Stream phase changes
    status = None
    while status != JobLifeCycle.RUNNING and not JobLifeCycle.is_done(status):
        job.refresh_from_db()
        if status != job.last_status:
            status = job.last_status
            await notify(consumer=consumer, message=get_status_message(status))
            if should_disconnect():
                return
        await asyncio.sleep(SOCKET_SLEEP)

    if JobLifeCycle.is_done(status):
        await notify(consumer=consumer, message=get_status_message(status))
        RedisToStream.remove_job_logs(job_uuid=job_uuid)
        return

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

        if should_disconnect():
            should_quite = True

        if should_quite:
            return

        await asyncio.sleep(SOCKET_SLEEP)


@authorized()
async def build_logs_v2(request,  # pylint:disable=too-many-branches
                        ws,
                        username,
                        project_name,
                        build_id):
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
                   actor_id=request.app.user.id,
                   actor_name=request.app.user.username)

    if job_uuid in request.app.job_logs_ws_managers:
        ws_manager = request.app.job_logs_ws_managers[job_uuid]
    else:
        ws_manager = SocketManager()
        request.app.job_logs_ws_managers[job_uuid] = ws_manager

    def handle_job_disconnected_ws(ws):
        ws_manager.remove_sockets(ws)
        if not ws_manager.ws:
            logger.info('Stopping resources monitor for uuid %s', job_uuid)
            request.app.job_logs_ws_managers.pop(job_uuid, None)

        logger.info('Quitting resources socket for uuid %s', job_uuid)

    def should_disconnect():
        return not ws_manager.ws

    pod_id = JOB_NAME_FORMAT.format(name=DOCKERIZER_JOB_NAME, job_uuid=job_uuid)
    ws_manager.add_socket(ws)
    should_quite = False

    # Stream phase changes
    status = None
    while status != JobLifeCycle.RUNNING and not JobLifeCycle.is_done(status):
        job.refresh_from_db()
        if status != job.last_status:
            status = job.last_status
            await notify(consumer=ws_manager, message=get_status_message(status))
            if should_disconnect():
                return
        await asyncio.sleep(SOCKET_SLEEP)

    if JobLifeCycle.is_done(status):
        await notify(consumer=ws_manager, message=get_status_message(status))
        return

    # Stream logs
    for message in stream_logs(pod_id=pod_id):
        if message:
            await notify(consumer=ws_manager, message=message)

        # Just to check if connection closed
        if ws._connection_lost:  # pylint:disable=protected-access
            handle_job_disconnected_ws(ws)
            should_quite = True

        if should_disconnect():
            should_quite = True

        if should_quite:
            return
        await asyncio.sleep(SOCKET_SLEEP)
