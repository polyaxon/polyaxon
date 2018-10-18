import asyncio

from websockets import ConnectionClosed

import auditor
from constants.experiments import ExperimentLifeCycle
from db.redis.to_stream import RedisToStream
from event_manager.events.experiment import EXPERIMENT_RESOURCES_VIEWED, EXPERIMENT_LOGS_VIEWED
from polyaxon.settings import CeleryQueues, RoutingKeys
from streams.authentication import authorized
from streams.constants import RESOURCES_CHECK, CHECK_DELAY, SOCKET_SLEEP, MAX_RETRIES
from streams.consumers import Consumer
from streams.logger import logger
from streams.resources.utils import get_error_message, get_status_message, notify
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

    if experiment_uuid in request.app.experiment_resources_ws_mangers:
        ws_manager = request.app.experiment_resources_ws_mangers[experiment_uuid]
    else:
        ws_manager = SocketManager()
        request.app.experiment_resources_ws_mangers[experiment_uuid] = ws_manager

    def handle_experiment_disconnected_ws(ws):
        ws_manager.remove_sockets(ws)
        if not ws_manager.ws:
            logger.info('Stopping resources monitor for uuid %s', experiment_uuid)
            RedisToStream.remove_experiment_resources(experiment_uuid=experiment_uuid)
            request.app.experiment_resources_ws_mangers.pop(experiment_uuid, None)

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
async def experiment_logs(request,  # pylint:disable=too-many-branches
                          ws,
                          username,
                          project_name,
                          experiment_id):
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
                   actor_id=request.app.user.id,
                   actor_name=request.app.user.username)

    if not RedisToStream.is_monitored_experiment_logs(experiment_uuid=experiment_uuid):
        logger.info('Experiment uuid `%s` logs is now being monitored', experiment_uuid)
        RedisToStream.monitor_experiment_logs(experiment_uuid=experiment_uuid)

    # start consumer
    if experiment_uuid in request.app.experiment_logs_consumers:
        consumer = request.app.experiment_logs_consumers[experiment_uuid]
    else:
        logger.info('Add experiment log consumer for %s', experiment_uuid)
        consumer = Consumer(
            routing_key='{}.{}.*'.format(RoutingKeys.LOGS_SIDECARS_EXPERIMENTS, experiment_uuid),
            queue='{}.{}'.format(CeleryQueues.STREAM_LOGS_SIDECARS, experiment_uuid))
        request.app.experiment_logs_consumers[experiment_uuid] = consumer
        consumer.run()

    def should_disconnect():
        if not consumer.ws:
            logger.info('Stopping logs monitor for experiment uuid %s', experiment_uuid)
            RedisToStream.remove_experiment_logs(experiment_uuid=experiment_uuid)
            # if experiment_uuid in request.app.experiment_logs_consumers:
            #     consumer = request.app.experiment_logs_consumers.pop(experiment_uuid, None)
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
    while status != ExperimentLifeCycle.RUNNING and not ExperimentLifeCycle.is_done(status):
        experiment.refresh_from_db()
        if status != experiment.last_status:
            status = experiment.last_status
            await notify(consumer=consumer, message=get_status_message(status))
            if should_disconnect():
                return
        await asyncio.sleep(SOCKET_SLEEP)

    if ExperimentLifeCycle.is_done(status):
        await notify(consumer=consumer, message=get_status_message(status))
        RedisToStream.remove_experiment_logs(experiment_uuid=experiment_uuid)
        return

    while True:
        num_message_retries += 1
        for message in consumer.get_messages():
            num_message_retries = 0
            await notify(consumer=consumer, message=message)

        # After trying a couple of time, we must check the status of the experiment
        if num_message_retries > MAX_RETRIES:
            experiment.refresh_from_db()
            if experiment.is_done:
                logger.info(
                    'removing all socket because the experiment `%s` is done', experiment_uuid)
                consumer.ws = set([])
            else:
                num_message_retries -= CHECK_DELAY

        # Just to check if connection closed
        if ws._connection_lost:  # pylint:disable=protected-access
            logger.info('Quitting logs socket for experiment uuid %s', experiment_uuid)
            consumer.remove_sockets({ws, })
            should_quite = True

        if should_disconnect():
            should_quite = True

        if should_quite:
            return

        await asyncio.sleep(SOCKET_SLEEP)
