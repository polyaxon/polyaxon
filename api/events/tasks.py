# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from polyaxon_schemas.experiment import JobStateConfig

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
    logger.info('handling events resources')
    print('persist:{}\npayload:{}'.format(persist, payload))
    logger.info(payload)


@celery_app.task(name=CeleryTasks.EVENTS_HANDLE_JOB_STATUSES)
def handle_events_job_statues(payload):
    # Validate the job state
    job_state = JobStateConfig.from_dict(payload)
    job_uuid = job_state.details.labels.job_id
    details = job_state.details.to_dict()
    logger.info('handling events status for job_uuid: {}, details: {} '.format(job_uuid, details))

    try:
        job = ExperimentJob.objects.get(uuid=job_uuid)
    except ExperimentJob.DoesNotExist:
        logger.info('Job uuid`{}` does not exist'.format(job_uuid))
        return

    # Set the new status
    job.set_status(status=job_state.status, message=job_state.message, details=details)


@celery_app.task(name=CeleryTasks.EVENTS_HANDLE_LOGS_SIDECAR)
def handle_events_job_logs(payload, persist):
    # must persist resources if logs according to the config
    logger.info('handling events job logs')
    print('persist:{}\npayload:{}'.format(persist, payload))
    logger.info(payload)
