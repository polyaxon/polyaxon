# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

import time

from polyaxon_k8s.constants import PodLifeCycle

from api.config_settings import CeleryPublishTask
from api.celery_api import app as celery_app
from libs.redis_db import RedisToStream
from events.tasks import handle_events_job_logs

logger = logging.getLogger('polyaxon.monitors.sidecar')


def run(k8s_manager, pod_id, container_job_name, persist):
    raw = k8s_manager.k8s_api.read_namespaced_pod_log(pod_id,
                                                      k8s_manager.namespace,
                                                      container=container_job_name,
                                                      follow=True,
                                                      _preload_content=False)
    for log_line in raw.stream():
        experiment_id = 0  # TODO extract experiment id
        logger.info("Publishing event: {}".format(log_line))
        handle_events_job_logs.delay(experiment_id=experiment_id,
                                     container_job_name=container_job_name,
                                     log_line=log_line,
                                     persist=persist)
        if (RedisToStream.is_monitored_job_logs(container_job_name) or
                RedisToStream.is_monitored_experiment_logs(experiment_id)):
            celery_app.send_task(CeleryPublishTask.PUBLISH_LOGS_SIDECAR,
                                 kwargs={'experiment_id': experiment_id,
                                         'container_job_name': container_job_name,
                                         'log_line': log_line})


def can_log(k8s_manager, pod_id, log_sleep_interval):
    status = k8s_manager.k8s_api.read_namespaced_pod_status(pod_id,
                                                            k8s_manager.namespace)
    logger.debug(status)
    while status.status.phase != PodLifeCycle.RUNNING:
        time.sleep(log_sleep_interval)
        status = k8s_manager.k8s_api.read_namespaced_pod_status(pod_id,
                                                                k8s_manager.namespace)
