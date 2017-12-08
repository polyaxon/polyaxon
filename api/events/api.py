# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import asyncio
import logging

from django.core.exceptions import ValidationError

from sanic import Sanic

from websockets import ConnectionClosed

from api.config_settings.celery_settings import RoutingKeys, CeleryQueues
from events.consumers import Consumer
from events.socket_manager import SocketManager
from experiments.models import ExperimentJob
from libs.redis_db import RedisToStream

logger = logging.getLogger('polyaxon.monitors.api')

app = Sanic(__name__)


def _get_job(job_uuid):
    try:
        job = ExperimentJob.objects.get(uuid=job_uuid)
    except (ExperimentJob.DoesNotExist, ValidationError):
        logger.info('Job with uuid `{}` does not exist'.format(job_uuid))
        return None

    if not job.is_running:
        logger.info('Job with uuid `{}` is not currently running'.format(job_uuid))
        return None

    return job


def handle_disconnected_ws(request, ws, job_uuid):
    request.app.job_resources_ws_manger.remove_sockets(ws)
    if len(request.app.job_resources_ws_manger.ws) == 0:
        RedisToStream.remove_job_resources(job_uuid=job_uuid)
        logger.info('Stopping resources monitor for job uuid {}'.format(job_uuid))

    logger.info('Quitting resources socket for job uuid {}'.format(job_uuid))


@app.websocket('/stream/v1/resources/job/<job_uuid>')
async def job_resources(request, ws, job_uuid):
    job = _get_job(job_uuid=job_uuid)

    if job is None:
        return

    if not RedisToStream.is_monitored_job_resources(job_uuid=job_uuid):
        logger.info('Job uuid `{}` is now being monitored'.format(job_uuid))
        RedisToStream.monitor_job_resources(job_uuid=job_uuid)

    request.app.job_resources_ws_manger.add_socket(ws)
    while True:
        resources = RedisToStream.get_latest_job_resources(job_uuid)
        if resources:
            try:
                await ws.send(resources)
            except ConnectionClosed:
                handle_disconnected_ws(request, ws, job_uuid)
                return

        # Just to check if connection closed
        try:
            await ws.recv()
        except ConnectionClosed:
            handle_disconnected_ws(request, ws, job_uuid)
            return
        await asyncio.sleep(1)


@app.websocket('/stream/v1/logs/job/<job_uuid>')
async def job_logs(request, ws, job_uuid):
    job = _get_job(job_uuid=job_uuid)

    if job is None:
        return

    if not RedisToStream.is_monitored_job_logs(job_uuid=job_uuid):
        logger.info('Job uuid `{}` logs is now being monitored'.format(job_uuid))
        RedisToStream.monitor_job_logs(job_uuid=job_uuid)

    # start consumer
    if request.app.logs_consumer is None:
        logger.info('Add log consumer'.format(job_uuid))
        request.app.logs_consumer = Consumer(
            routing_key='{}.{}.{}'.format(RoutingKeys.LOGS_SIDECARS,
                                          job.experiment.uuid.hex,
                                          job_uuid),
            queue=CeleryQueues.STREAM_LOGS_SIDECARS)
        request.app.logs_consumer.run()

    # add socket manager
    request.app.logs_consumer.add_socket(ws)
    should_quite = False
    while True:
        for message in request.app.logs_consumer.get_messages():
            disconnected_ws = set()
            for _ws in request.app.logs_consumer.ws:
                try:
                    await _ws.send(message)
                except ConnectionClosed:
                    disconnected_ws.add(_ws)
            request.app.logs_consumer.remove_sockets(disconnected_ws)

        # Just to check if connection closed
        try:
            await ws.recv()
        except ConnectionClosed:
            logger.info('Quitting logs socket for job uuid {}'.format(job_uuid))
            request.app.logs_consumer.remove_sockets({ws, })
            should_quite = True

        if len(request.app.logs_consumer.ws) == 0:
            RedisToStream.remove_job_logs(job_uuid=job_uuid)
            logger.info('Stopping logs monitor for job uuid {}'.format(job_uuid))
            should_quite = True

        if should_quite:
            return

        await asyncio.sleep(1)


@app.listener('after_server_start')
async def notify_server_started(app, loop):
    app.job_resources_ws_manger = SocketManager()
    app.logs_consumer = None


@app.listener('after_server_stop')
async def notifiy_server_stoped(app, loop):
    del app.job_resources_ws_manger
    if app.logs_consumer:
        app.logs_consumer.stop()
