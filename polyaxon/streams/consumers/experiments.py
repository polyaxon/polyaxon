import asyncio

import auditor

from constants.experiments import ExperimentLifeCycle
from db.redis.to_stream import RedisToStream
from event_manager.events.experiment import EXPERIMENT_LOGS_VIEWED
from polyaxon.settings import CeleryQueues, RoutingKeys
from streams.authentication import authorized
from streams.constants import CHECK_DELAY, MAX_RETRIES, SOCKET_SLEEP
from streams.logger import logger
from streams.resources.utils import get_error_message, get_status_message, notify
from streams.validation.experiment import validate_experiment


@authorized()
async def experiment_logs(request,  # pylint:disable=too-many-branches
                          ws,
                          username,
                          project_name,
                          experiment_id):
    from streams.consumers.consumers import Consumer

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
            routing_key='{}.{}.*'.format(RoutingKeys.STREAM_LOGS_SIDECARS_EXPERIMENTS,
                                         experiment_uuid),
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
            await notify(ws_manager=consumer, message=get_status_message(status))
            if should_disconnect():
                return
        await asyncio.sleep(SOCKET_SLEEP)

    if ExperimentLifeCycle.is_done(status):
        await notify(ws_manager=consumer, message=get_status_message(status))
        RedisToStream.remove_experiment_logs(experiment_uuid=experiment_uuid)
        return

    while True:
        num_message_retries += 1
        for message in consumer.get_messages():
            num_message_retries = 0
            await notify(ws_manager=consumer, message=message)

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
