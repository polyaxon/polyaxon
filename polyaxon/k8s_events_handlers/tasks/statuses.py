from typing import Any, Dict

from django.db import IntegrityError

import conf

from db.models.build_jobs import BuildJob
from db.models.experiment_jobs import ExperimentJob
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.notebooks import NotebookJob
from db.models.projects import Project
from db.models.tensorboards import TensorboardJob
from k8s_events_handlers.tasks.logger import logger
from polyaxon.celery_api import celery_app
from polyaxon.settings import Intervals, K8SEventsCeleryTasks


def set_node_scheduling(job: Any, node_name: str) -> None:
    if job.node_scheduled or node_name is None:
        return
    job.node_scheduled = node_name
    job.save(update_fields=['node_scheduled'])


@celery_app.task(name=K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_EXPERIMENT_JOB_STATUSES,
                 bind=True,
                 max_retries=3,
                 ignore_result=True)
def k8s_events_handle_experiment_job_statuses(self: 'celery_app.task', payload: Dict) -> None:
    """Experiment jobs statuses"""
    details = payload['details']
    job_uuid = details['labels']['job_uuid']
    logger.debug('handling events status for job_uuid: %s, status: %s',
                 job_uuid, payload['status'])

    try:
        job = ExperimentJob.objects.get(uuid=job_uuid)
    except ExperimentJob.DoesNotExist:
        logger.debug('Job uuid`%s` does not exist', job_uuid)
        return

    try:
        job.experiment
    except Experiment.DoesNotExist:
        logger.debug('Experiment for job `%s` does not exist anymore', job_uuid)
        return

    if job.last_status is None and self.request.retries < 2:
        self.retry(countdown=1)

    # Set the new status
    try:
        set_node_scheduling(job, details['node_name'])
        job.set_status(status=payload['status'],
                       message=payload['message'],
                       created_at=payload.get('created_at'),
                       traceback=payload.get('traceback'),
                       details=details)
        logger.debug('status %s is set for job %s %s', payload['status'], job_uuid, job.id)
    except IntegrityError:
        # Due to concurrency this could happen, we just retry it
        logger.info('Retry job status %s handling %s', payload['status'], job_uuid)
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)


@celery_app.task(name=K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_JOB_STATUSES,
                 bind=True,
                 max_retries=3,
                 ignore_result=True)
def k8s_events_handle_job_statuses(self: 'celery_app.task', payload: Dict) -> None:
    """Project jobs statuses"""
    details = payload['details']
    job_uuid = details['labels']['job_uuid']
    job_name = details['labels']['job_name']
    project_name = details['labels'].get('project_name')
    logger.debug('handling events status for job %s', job_name)

    try:
        job = Job.objects.get(uuid=job_uuid)
    except Job.DoesNotExist:
        logger.debug('Job `%s` does not exist', job_name)
        return

    try:
        job.project
    except Project.DoesNotExist:
        logger.debug('Project for job `%s` does not exist', project_name)
        return

    # Set the new status
    try:
        set_node_scheduling(job, details['node_name'])
        job.set_status(status=payload['status'],
                       message=payload['message'],
                       traceback=payload.get('traceback'),
                       details=details)
    except IntegrityError:
        # Due to concurrency this could happen, we just retry it
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)


@celery_app.task(name=K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_PLUGIN_JOB_STATUSES,
                 bind=True,
                 max_retries=3,
                 ignore_result=True)
def k8s_events_handle_plugin_job_statuses(self: 'celery_app.task', payload: Dict) -> None:
    """Project Plugin jobs statuses"""
    details = payload['details']
    app = details['labels']['app']
    job_uuid = details['labels']['job_uuid']
    job_name = details['labels']['job_name']
    project_name = details['labels'].get('project_name')
    logger.debug('handling events status for job %s %s', job_name, app)

    try:
        if app == conf.get('APP_LABELS_TENSORBOARD'):
            job = TensorboardJob.objects.get(uuid=job_uuid)
        elif app == conf.get('APP_LABELS_NOTEBOOK'):
            job = NotebookJob.objects.get(uuid=job_uuid)
        else:
            logger.info('Plugin job `%s` does not exist', app)
            return
    except (NotebookJob.DoesNotExist, TensorboardJob.DoesNotExist):
        logger.debug('`%s - %s` does not exist', app, job_name)
        return

    try:
        job.project
    except Project.DoesNotExist:
        logger.debug('`%s` does not exist anymore', project_name)

    # Set the new status
    try:
        set_node_scheduling(job, details['node_name'])
        job.set_status(status=payload['status'],
                       message=payload['message'],
                       traceback=payload.get('traceback'),
                       details=details)
    except IntegrityError:
        # Due to concurrency this could happen, we just retry it
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)


@celery_app.task(name=K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_BUILD_JOB_STATUSES,
                 bind=True,
                 max_retries=3,
                 ignore_result=True)
def k8s_events_handle_build_job_statuses(self: 'celery_app.task', payload: Dict) -> None:
    """Project Plugin jobs statuses"""
    details = payload['details']
    app = details['labels']['app']
    job_uuid = details['labels']['job_uuid']
    job_name = details['labels']['job_name']
    project_name = details['labels'].get('project_name')
    logger.debug('handling events status for build jon %s %s', job_name, app)

    try:
        build_job = BuildJob.objects.get(uuid=job_uuid)
    except BuildJob.DoesNotExist:
        logger.info('Build job `%s` does not exist', job_name)
        return

    try:
        build_job.project
    except Project.DoesNotExist:
        logger.debug('`%s` does not exist anymore', project_name)

    # Set the new status
    try:
        set_node_scheduling(build_job, details['node_name'])
        build_job.set_status(status=payload['status'],
                             message=payload['message'],
                             traceback=payload.get('traceback'),
                             details=details)
    except IntegrityError:
        # Due to concurrency this could happen, we just retry it
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)
