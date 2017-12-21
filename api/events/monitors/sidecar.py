# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

import time

from django.conf import settings
from polyaxon_schemas.experiment import JobLabelConfig

from api.config_settings import RoutingKeys
from api.celery_api import app as celery_app
from libs.redis_db import RedisToStream
from events.tasks import handle_events_job_logs
from spawner.utils.constants import PodLifeCycle

logger = logging.getLogger('polyaxon.monitors.sidecar')


def run(k8s_manager, pod_id, experiment_uuid, job_uuid, container_job_name, persist):
    raw = k8s_manager.k8s_api.read_namespaced_pod_log(pod_id,
                                                      k8s_manager.namespace,
                                                      container=container_job_name,
                                                      follow=True,
                                                      _preload_content=False)
    for log_line in raw.stream():
        log_line = log_line.decode('utf-8')
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
                        'log_line': log_line
                    },
                    routing_key='{}.{}.{}'.format(RoutingKeys.LOGS_SIDECARS,
                                                  experiment_uuid,
                                                  job_uuid),
                    exchange=settings.INTERNAL_EXCHANGE,
                )


def can_log(k8s_manager, pod_id, log_sleep_interval):
    status = k8s_manager.k8s_api.read_namespaced_pod_status(pod_id,
                                                            k8s_manager.namespace)
    logger.debug(status)
    labels = status.metadata.labels
    while status.status.phase != PodLifeCycle.RUNNING:
        time.sleep(log_sleep_interval)
        status = k8s_manager.k8s_api.read_namespaced_pod_status(pod_id,
                                                                k8s_manager.namespace)
        labels = status.metadata.labels

    return JobLabelConfig.from_dict(labels)
