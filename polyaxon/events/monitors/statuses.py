# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from django.conf import settings

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


def get_label_selector():
    type_label = settings.TYPE_LABELS_EXPERIMENT
    return 'role in ({},{}),type={}'.format(
        settings.ROLE_LABELS_WORKER,
        settings.ROLE_LABELS_DASHBOARD,
        type_label)


def run(k8s_manager):
    w = watch.Watch()

    for event in w.stream(k8s_manager.k8s_api.list_namespaced_pod,
                          namespace=k8s_manager.namespace,
                          label_selector=get_label_selector()):
        logger.debug("Received event: {}".format(event['type']))
        event_object = event['object'].to_dict()
        job_state = get_job_state(
            event_type=event['type'],
            event=event_object,
            job_container_names=(settings.CONTAINER_NAME_JOB, settings.CONTAINER_NAME_PLUGIN_JOB),
            experiment_type_label=settings.TYPE_LABELS_EXPERIMENT)

        if job_state:
            status = job_state.status
            labels = None
            if job_state.details and job_state.details.labels:
                labels = job_state.details.labels.to_dict()
            logger.info("Updating job container {}, {}".format(status, labels))
            logger.debug(event_object)
            job_state = job_state.to_dict()
            logger.debug(job_state)
            # Only update job containers if it's an experiment job not plugins
            if settings.CONTAINER_NAME_JOB in job_state['details']['container_statuses']:
                update_job_containers(event_object, status, settings.CONTAINER_NAME_JOB)
                # Handle experiment job statuses differently than plugin job statuses
                handle_events_job_statues.delay(payload=job_state)
            elif settings.CONTAINER_NAME_PLUGIN_JOB in job_state['details']['container_statuses']:
                # Handle plugin job statuses
                handle_events_job_statues.delay(payload=job_state)
