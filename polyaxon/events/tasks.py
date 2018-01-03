# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from api.settings import CeleryTasks
from api.celery_api import app as celery_app
from clusters.models import ClusterEvent
from experiments.models import ExperimentJob

logger = logging.getLogger('polyaxon.tasks.events')


@celery_app.task(name=CeleryTasks.EVENTS_HANDLE_NAMESPACE)
def handle_events_namespace(cluster_id, payload):
    logger.info('handling events namespace for cluster: {}'.format(cluster_id))
    ClusterEvent.objects.create(cluster_id=cluster_id, **payload)


@celery_app.task(name=CeleryTasks.EVENTS_HANDLE_RESOURCES)
def handle_events_resources(payload, persist):
    # here we must persist resources if requested
    logger.info('handling events resources with persist:{}'.format(persist))
    logger.info(payload)


@celery_app.task(name=CeleryTasks.EVENTS_HANDLE_JOB_STATUSES)
def handle_events_job_statues(payload):
    details = payload['details']
    job_uuid = details['labels']['job_uuid']
    logger.info('handling events status for job_uuid: {}'.format(job_uuid))

    try:
        job = ExperimentJob.objects.get(uuid=job_uuid)
    except ExperimentJob.DoesNotExist:
        logger.info('Job uuid`{}` does not exist'.format(job_uuid))
        return

    # Set the new status
    job.set_status(status=payload['status'], message=payload['message'], details=details)


@celery_app.task(name=CeleryTasks.EVENTS_HANDLE_LOGS_SIDECAR)
def handle_events_job_logs(experiment_uuid, job_uuid, log_line, persist):
    # must persist resources if logs according to the config
    logger.info('handling log event for {} {} {}'.format(
        experiment_uuid, job_uuid, persist))
