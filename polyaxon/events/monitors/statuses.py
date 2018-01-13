# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from kubernetes import watch

from libs.redis_db import RedisJobContainers
from events.tasks import handle_events_job_statues
from spawner.utils.constants import JobLifeCycle
from spawner.utils.jobs import get_job_state

logger = logging.getLogger('polyaxon.monitors.statuses')


def update_job_containers(event, status, job_container_name):
    if JobLifeCycle.is_done(status):
        # Remove the job monitoring
        job_uuid = event['metadata']['labels']['job_uuid']
        logger.info('Stop monitoring job_uuid: {}'.format(job_uuid))
        RedisJobContainers.remove_job(job_uuid)

    if event['status']['container_statuses'] is None:
        return

    def get_container_id(container_id):
        if not container_id:
            return None
        if container_id.startswith('docker://'):
            return container_id[len('docker://'):]
        return container_id

    for container_status in event['status']['container_statuses']:
        if container_status['name'] != job_container_name:
            continue

        container_id = get_container_id(container_status['container_id'])
        if container_id:
            job_uuid = event['metadata']['labels']['job_uuid']
            if container_status['state']['running'] is not None:
                logger.info('Monitoring (container_id, job_uuid): ({}, {})'.format(container_id,
                                                                                   job_uuid))
                RedisJobContainers.monitor(container_id=container_id, job_uuid=job_uuid)
            else:

                RedisJobContainers.remove_container(container_id=container_id)


def run(k8s_manager, experiment_type_label, job_container_name, label_selector=None):
    w = watch.Watch()

    for event in w.stream(k8s_manager.k8s_api.list_namespaced_pod,
                          namespace=k8s_manager.namespace,
                          label_selector=label_selector):
        logger.debug("Received event: {}".format(event['type']))
        event_object = event['object'].to_dict()
        job_state = get_job_state(event_type=event['type'],
                                  event=event_object,
                                  job_container_name=job_container_name,
                                  experiment_type_label=experiment_type_label)

        if job_state:
            status = job_state.status
            labels = None
            if job_state.details and job_state.details.labels:
                labels = job_state.details.labels.to_dict()
            logger.info("Updating job container {}, {}".format(status, labels))
            job_state = job_state.to_dict()
            logger.debug(event_object)
            update_job_containers(event_object, status, job_container_name)
            logger.debug(job_state)
            handle_events_job_statues.delay(payload=job_state)
