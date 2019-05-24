import asyncio

from websockets import ConnectionClosed

import auditor
import conf

from constants.experiment_jobs import get_experiment_job_container_name
from db.redis.to_stream import RedisToStream
from events.registry.experiment_job import (
    EXPERIMENT_JOB_LOGS_VIEWED,
    EXPERIMENT_JOB_RESOURCES_VIEWED
)
from options.registry.k8s import K8S_NAMESPACE
from streams.authentication import authorized
from streams.constants import CHECK_DELAY, RESOURCES_CHECK, SOCKET_SLEEP
from streams.logger import logger
from streams.resources.logs import log_job
from streams.resources.utils import get_error_message
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

    if job_uuid in request.app.job_resources_ws_managers:
        ws_manager = request.app.job_resources_ws_managers[job_uuid]
    else:
        ws_manager = SocketManager()
        request.app.job_resources_ws_managers[job_uuid] = ws_manager

    def handle_job_disconnected_ws(ws):
        ws_manager.remove_sockets(ws)
        if not ws_manager.ws:
            logger.info('Stopping resources monitor for job %s', job_name)
            RedisToStream.remove_job_resources(job_uuid=job_uuid)
            request.app.job_resources_ws_managers.pop(job_uuid, None)

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
async def experiment_job_logs_v2(request, ws, username, project_name, experiment_id, job_id):
    job, experiment, message = validate_experiment_job(request=request,
                                                       username=username,
                                                       project_name=project_name,
                                                       experiment_id=experiment_id,
                                                       job_id=job_id)
    if job is None:
        await ws.send(get_error_message(message))
        return

    pod_id = job.pod_id

    container_job_name = get_experiment_job_container_name(backend=experiment.backend,
                                                           framework=experiment.framework)

    auditor.record(event_type=EXPERIMENT_JOB_LOGS_VIEWED,
                   instance=job,
                   actor_id=request.app.user.id,
                   actor_name=request.app.user.username)

    # Stream logs
    await log_job(request=request,
                  ws=ws,
                  job=job,
                  pod_id=pod_id,
                  container=container_job_name,
                  namespace=conf.get(K8S_NAMESPACE))
