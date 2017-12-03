# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

import time

from api.config_settings import CeleryPublishTask
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
        logger.info("Publishing event: {}".format(log_line))
        handle_events_job_logs.delay(experiment_uuid=experiment_uuid,
                                     container_job_name=container_job_name,
                                     log_line=log_line,
                                     persist=persist)
        if (RedisToStream.is_monitored_job_logs(job_uuid) or
                RedisToStream.is_monitored_experiment_logs(experiment_uuid)):
            celery_app.send_task(CeleryPublishTask.PUBLISH_LOGS_SIDECAR,
                                 kwargs={'experiment_uuid': experiment_uuid,
                                         'container_job_name': container_job_name,
                                         'log_line': log_line})


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

    return labels
