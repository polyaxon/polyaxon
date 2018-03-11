# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from amqp import AMQPError
from django.conf import settings
from redis import RedisError

from polyaxon.config_settings import RoutingKeys
from polyaxon.celery_api import app as celery_app
from libs.redis_db import RedisToStream
from events.tasks import handle_events_job_logs

logger = logging.getLogger('polyaxon.monitors.publisher')


def publish_log(log_line,
                status,
                experiment_uuid,
                experiment_name,
                job_uuid,
                task_type=None,
                task_idx=None):
    try:
        log_line = log_line.decode('utf-8')
    except AttributeError:
        pass

    logger.info("Publishing log event for task: {}.{}, {}".format(task_type,
                                                                  task_idx,
                                                                  experiment_name))
    handle_events_job_logs.delay(experiment_name=experiment_name,
                                 experiment_uuid=experiment_uuid,
                                 job_uuid=job_uuid,
                                 log_line=log_line,
                                 task_type=task_type,
                                 task_idx=task_idx)
    try:
        should_stream = (RedisToStream.is_monitored_job_logs(job_uuid) or
                         RedisToStream.is_monitored_experiment_logs(experiment_uuid))
    except RedisError:
        should_stream = False
    if should_stream:
        logger.info("Streaming new log event for experiment: {}".format(experiment_uuid))

        with celery_app.producer_or_acquire(None) as producer:
            try:
                producer.publish(
                    {
                        'experiment_uuid': experiment_uuid,
                        'job_uuid': job_uuid,
                        'log_line': log_line,
                        'status': status,
                        'task_type': task_type,
                        'task_idx': task_idx
                    },
                    routing_key='{}.{}.{}'.format(RoutingKeys.LOGS_SIDECARS,
                                                  experiment_uuid,
                                                  job_uuid),
                    exchange=settings.INTERNAL_EXCHANGE,
                )
            except (TimeoutError, AMQPError):
                pass

