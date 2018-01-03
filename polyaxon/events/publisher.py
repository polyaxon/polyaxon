# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from django.conf import settings

from api.config_settings import RoutingKeys
from api.celery_api import app as celery_app
from libs.redis_db import RedisToStream
from events.tasks import handle_events_job_logs

logger = logging.getLogger('polyaxon.monitors.publisher')


def publish_log(log_line,
                status,
                experiment_uuid,
                job_uuid,
                persist=False,
                task_type=None,
                task_idx=None):
    try:
        log_line = log_line.decode('utf-8')
    except AttributeError:
        pass

    logger.info("Publishing log event for experiment: {}, {}".format(job_uuid, experiment_uuid))
    handle_events_job_logs.delay(experiment_uuid=experiment_uuid,
                                 job_uuid=job_uuid,
                                 log_line=log_line,
                                 persist=persist)
    if (RedisToStream.is_monitored_job_logs(job_uuid) or
            RedisToStream.is_monitored_experiment_logs(experiment_uuid)):
        logger.info("Streaming new log event for experiment: {}".format(experiment_uuid))

        with celery_app.producer_or_acquire(None) as producer:
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
