import asyncio

from websockets import ConnectionClosed

import auditor
import conf

from constants.experiment_jobs import get_experiment_job_container_name
from db.redis.to_stream import RedisToStream
from events.registry.experiment import EXPERIMENT_LOGS_VIEWED, EXPERIMENT_RESOURCES_VIEWED
from options.registry.k8s import K8S_NAMESPACE
from streams.authentication import authorized
from streams.constants import CHECK_DELAY, RESOURCES_CHECK, SOCKET_SLEEP
from streams.logger import logger
from streams.resources.logs import log_experiment
from streams.resources.utils import get_error_message
from streams.socket_manager import SocketManager
from streams.validation.experiment import validate_experiment


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
                   actor_id=request.app.user.id,
                   actor_name=request.app.user.username)

    if not RedisToStream.is_monitored_experiment_resources(experiment_uuid=experiment_uuid):
        logger.info('Experiment resource with uuid `%s` is now being monitored', experiment_uuid)
        RedisToStream.monitor_experiment_resources(experiment_uuid=experiment_uuid)

    if experiment_uuid in request.app.experiment_resources_ws_managers:
        ws_manager = request.app.experiment_resources_ws_managers[experiment_uuid]
    else:
        ws_manager = SocketManager()
        request.app.experiment_resources_ws_managers[experiment_uuid] = ws_manager

    def handle_experiment_disconnected_ws(ws):
        ws_manager.remove_sockets(ws)
        if not ws_manager.ws:
            logger.info('Stopping resources monitor for uuid %s', experiment_uuid)
            RedisToStream.remove_experiment_resources(experiment_uuid=experiment_uuid)
            request.app.experiment_resources_ws_managers.pop(experiment_uuid, None)

        logger.info('Quitting resources socket for uuid %s', experiment_uuid)

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
                logger.info(
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
async def experiment_logs_v2(request, ws, username, project_name, experiment_id):
    experiment, message = validate_experiment(request=request,
                                              username=username,
                                              project_name=project_name,
                                              experiment_id=experiment_id)
    if experiment is None:
        await ws.send(get_error_message(message))
        return

    auditor.record(event_type=EXPERIMENT_LOGS_VIEWED,
                   instance=experiment,
                   actor_id=request.app.user.id,
                   actor_name=request.app.user.username)

    container_job_name = get_experiment_job_container_name(backend=experiment.backend,
                                                           framework=experiment.framework)

    # Stream logs
    await log_experiment(request=request,
                         ws=ws,
                         experiment=experiment,
                         container=container_job_name,
                         namespace=conf.get(K8S_NAMESPACE))
