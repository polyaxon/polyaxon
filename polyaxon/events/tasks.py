# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from experiments.utils import get_experiment_logs_path, create_experiment_logs_path
from polyaxon.settings import CeleryTasks
from polyaxon.celery_api import app as celery_app
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
def handle_events_job_logs(experiment_name,
                           experiment_uuid,
                           job_uuid,
                           log_line,
                           persist,
                           task_type=None,
                           task_idx=None):
    # must persist resources if logs according to the config
    logger.debug('handling log event for {} {} {}'.format(
        experiment_uuid, job_uuid, persist))
    if task_type and task_idx:
        log_line = '{}.{} -- {}'.format(task_type, int(task_idx) + 1, log_line)
    xp_logger = logging.getLogger(experiment_name)
    if not xp_logger.handlers:
        log_path = get_experiment_logs_path(experiment_name)
        log_handler = logging.FileHandler(log_path)
        log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        log_handler.setFormatter(log_formatter)
        xp_logger.addHandler(log_handler)

    xp_logger.setLevel(logging.INFO)
    xp_logger.info(log_line)
