# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import os
import time

from django.conf import settings

from polyaxon_k8s.constants import PodLifeCycle
from polyaxon_k8s.manager import K8SManager

from api.config_settings import CeleryPublishTask
from api.celery_api import app as celery_app
from libs.redis_db import RedisToStream
from events.tasks import handle_events_job_logs

logger = logging.getLogger('polyaxon.monitors.sidecar')


def run(k8s_manager, pod_id, job_id):
    raw = k8s_manager.k8s_api.read_namespaced_pod_log(pod_id,
                                                      k8s_manager.namespace,
                                                      container=job_id,
                                                      follow=True,
                                                      _preload_content=False)
    for log_line in raw.stream():
        experiment_id = 0  # TODO extract experiment id
        logger.info("Publishing event: {}".format(log_line))
        handle_events_job_logs.delay(experiment_id=experiment_id,
                                     job_id=job_id,
                                     log_line=log_line,
                                     persist=settings.PERSIST_EVENTS)
        if (RedisToStream.is_monitored_job_logs(job_id) or
                RedisToStream.is_monitored_experiment_logs(experiment_id)):
            celery_app.send_task(CeleryPublishTask.PUBLISH_LOGS_SIDECAR,
                                 kwargs={'experiment_id': experiment_id,
                                         'job_id': job_id,
                                         'log_line': log_line})


def can_log(k8s_manager, pod_id):
    status = k8s_manager.k8s_api.read_namespaced_pod_status(pod_id,
                                                            k8s_manager.namespace)
    logger.debug(status)
    while status.status.phase != PodLifeCycle.RUNNING:
        time.sleep(settings.LOG_SLEEP_INTERVAL)
        status = k8s_manager.k8s_api.read_namespaced_pod_status(pod_id,
                                                                k8s_manager.namespace)


def main():
    pod_id = os.environ['POLYAXON_POD_ID']
    job_id = os.environ['POLYAXON_JOB_ID']
    k8s_manager = K8SManager(namespace=settings.NAMESPACE, in_cluster=True)
    can_log(k8s_manager, pod_id)
    run(k8s_manager, pod_id, job_id)
    logger.debug('Finished logging')


if __name__ == '__main__':
    main()
