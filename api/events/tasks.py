# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from api.settings import CeleryTasks
from api.celery_api import app as celery_app
from clusters.models import ClusterErrors

logger = logging.getLogger('polyaxon.tasks.events')


@celery_app.task(name=CeleryTasks.EVENTS_HANDLE_NAMESPACE)
def handle_events_namespace(cluster_id, payload, persist):
    logger.info('handling events namespace for cluster: {}'.format(cluster_id))
    ClusterErrors.objects.create(cluster_id=cluster_id,
                                 created_at=payload['creation_timestamp'],
                                 data=payload['data'],
                                 meta=payload['meta'],
                                 level=payload['level'])


@celery_app.task(name=CeleryTasks.EVENTS_HANDLE_RESOURCES)
def handle_events_resources(payload, persist):
    # here we must persist resources if requested
    logger.info('handling events resources')
    print('persist:{}\npayload:{}'.format(persist, payload))
    logger.info(payload)


@celery_app.task(name=CeleryTasks.EVENTS_HANDLE_JOB_STATUSES)
def handle_events_job_statues(payload, persist):
    labels = payload['details']['labels']

    # update ExperimentJobStatus according to the new values
    logger.info('handling events statuses')
    print('persist:{}\npayload:{}'.format(persist, payload))
    logger.info(payload)


@celery_app.task(name=CeleryTasks.EVENTS_HANDLE_LOGS_SIDECAR)
def handle_events_job_logs(payload, persist):
    # must persist resources if logs according to the config
    logger.info('handling events job logs')
    print('persist:{}\npayload:{}'.format(persist, payload))
    logger.info(payload)
