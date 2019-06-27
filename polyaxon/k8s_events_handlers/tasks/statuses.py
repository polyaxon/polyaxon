from typing import Any, Dict

from django.db import IntegrityError

import conf
import workers

from db.models.build_jobs import BuildJob
from db.models.experiment_jobs import ExperimentJob
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.notebooks import NotebookJob
from db.models.projects import Project
from db.models.tensorboards import TensorboardJob
from db.redis.statuses import RedisStatuses
from k8s_events_handlers.tasks.logger import logger
from lifecycles.jobs import JobLifeCycle
from options.registry.restarts import (
    MAX_RESTARTS_BUILD_JOBS,
    MAX_RESTARTS_EXPERIMENTS,
    MAX_RESTARTS_JOBS,
    MAX_RESTARTS_NOTEBOOKS,
    MAX_RESTARTS_TENSORBOARDS
)
from options.registry.spawner import APP_LABELS_NOTEBOOK, APP_LABELS_TENSORBOARD
from polyaxon.settings import Intervals, K8SEventsCeleryTasks


def set_node_scheduling(job: Any, node_name: str) -> None:
    if job.node_scheduled or node_name is None:
        return
    job.node_scheduled = node_name
    job.save(update_fields=['node_scheduled'])


@workers.app.task(name=K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_EXPERIMENT_JOB_STATUSES,
                  bind=True,
                  max_retries=3,
                  ignore_result=True)
def k8s_events_handle_experiment_job_statuses(self: 'workers.app.task', payload: Dict) -> None:
    """Experiment jobs statuses"""
    details = payload['details']
    job_uuid = details['labels']['job_uuid']
    restart_count = payload.get('restart_count', 0)
    logger.debug('handling events status for job_uuid: %s, status: %s',
                 job_uuid, payload['status'])

    try:
        job = ExperimentJob.objects.get(uuid=job_uuid)
    except ExperimentJob.DoesNotExist:
        logger.debug('Job uuid`%s` does not exist', job_uuid)
        return

    try:
        experiment = job.experiment
    except Experiment.DoesNotExist:
        logger.debug('Experiment for job `%s` does not exist anymore', job_uuid)
        return

    if job.last_status is None and self.request.retries < 2:
        self.retry(countdown=1)

    max_restarts = experiment.max_restarts or conf.get(MAX_RESTARTS_EXPERIMENTS)
    if JobLifeCycle.failed(payload['status']) and restart_count < max_restarts:
        return

    # Set the new status
    try:
        RedisStatuses.set_status(job_uuid, payload['status'])
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


@workers.app.task(name=K8SEventsCeleryTasks.K8S_EVENTS_RECONCILE_EXPERIMENT_JOB_STATUSES,
                  ignore_result=True)
def k8s_events_reconcile_experiment_job_statuses(job_id, status, created_at) -> None:
    try:
        job = ExperimentJob.objects.get(id=job_id)
    except ExperimentJob.DoesNotExist:
        logger.debug('Job `%s` does not exist', job_id)
        return

    if job.is_done:
        return

    job.set_status(status=status,
                   message='Status was reconciled.',
                   created_at=created_at)


@workers.app.task(name=K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_JOB_STATUSES,
                  bind=True,
                  max_retries=3,
                  ignore_result=True)
def k8s_events_handle_job_statuses(self: 'workers.app.task', payload: Dict) -> None:
    """Project jobs statuses"""
    details = payload['details']
    job_uuid = details['labels']['job_uuid']
    job_name = details['labels']['job_name']
    restart_count = payload.get('restart_count', 0)
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

    max_restarts = job.max_restarts or conf.get(MAX_RESTARTS_JOBS)
    if JobLifeCycle.failed(payload['status']) and restart_count < max_restarts:
        return

    # Set the new status
    try:
        RedisStatuses.set_status(job_uuid, payload['status'])
        set_node_scheduling(job, details['node_name'])
        job.set_status(status=payload['status'],
                       message=payload['message'],
                       traceback=payload.get('traceback'),
                       details=details)
    except IntegrityError:
        # Due to concurrency this could happen, we just retry it
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)


@workers.app.task(name=K8SEventsCeleryTasks.K8S_EVENTS_RECONCILE_JOB_STATUSES,
                  ignore_result=True)
def k8s_events_reconcile_job_statuses(job_id, status, created_at) -> None:
    try:
        job = Job.objects.get(id=job_id)
    except ExperimentJob.DoesNotExist:
        logger.debug('Job `%s` does not exist', job_id)
        return

    if job.is_done:
        return

    job.set_status(status=status,
                   message='Status was reconciled.',
                   created_at=created_at)


def get_plugin_job(app, job_uuid=None, job_id=None):
    kwargs = {}
    if job_uuid:
        kwargs['uuid'] = job_uuid
    if job_id:
        kwargs['job_id'] = job_id

    try:
        if app == conf.get(APP_LABELS_TENSORBOARD):
            return TensorboardJob.objects.get(**kwargs)
        elif app == conf.get(APP_LABELS_NOTEBOOK):
            return NotebookJob.objects.get(**kwargs)
        logger.info('Plugin job `%s` does not exist', app)
    except (NotebookJob.DoesNotExist, TensorboardJob.DoesNotExist):
        return


def get_plugin_max_restarts(app, job):
    max_restarts = job.max_restarts or 0
    if not max_restarts:
        return conf.get(MAX_RESTARTS_TENSORBOARDS)
    elif app == conf.get(APP_LABELS_NOTEBOOK):
        return conf.get(MAX_RESTARTS_NOTEBOOKS)
    return max_restarts


@workers.app.task(name=K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_PLUGIN_JOB_STATUSES,
                  bind=True,
                  max_retries=3,
                  ignore_result=True)
def k8s_events_handle_plugin_job_statuses(self: 'workers.app.task', payload: Dict) -> None:
    """Project Plugin jobs statuses"""
    details = payload['details']
    app = details['labels']['app']
    job_uuid = details['labels']['job_uuid']
    job_name = details['labels']['job_name']
    restart_count = payload.get('restart_count', 0)
    project_name = details['labels'].get('project_name')
    logger.debug('handling events status for job %s %s', job_name, app)

    job = get_plugin_job(app=app, job_uuid=job_uuid)

    if not job:
        logger.debug('`%s - %s` does not exist', app, job_name)
        return

    try:
        job.project
    except Project.DoesNotExist:
        logger.debug('`%s` does not exist anymore', project_name)

    max_restarts = get_plugin_max_restarts(app, job)
    if JobLifeCycle.failed(payload['status']) and restart_count < max_restarts:
        return

    # Set the new status
    try:
        RedisStatuses.set_status(job_uuid, payload['status'])
        set_node_scheduling(job, details['node_name'])
        job.set_status(status=payload['status'],
                       message=payload['message'],
                       traceback=payload.get('traceback'),
                       details=details)
    except IntegrityError:
        # Due to concurrency this could happen, we just retry it
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)


@workers.app.task(name=K8SEventsCeleryTasks.K8S_EVENTS_RECONCILE_PLUGIN_JOB_STATUSES,
                  ignore_result=True)
def k8s_events_reconcile_plugin_job_statuses(job_id, app, status, created_at) -> None:
    job = get_plugin_job(app=app, job_uuid=job_id)

    if not job:
        logger.debug('Job `%s` does not exist', job_id)
        return

    if job.is_done:
        return

    job.set_status(status=status,
                   message='Status was reconciled.',
                   created_at=created_at)


@workers.app.task(name=K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_BUILD_JOB_STATUSES,
                  bind=True,
                  max_retries=3,
                  ignore_result=True)
def k8s_events_handle_build_job_statuses(self: 'workers.app.task', payload: Dict) -> None:
    """Project Plugin jobs statuses"""
    details = payload['details']
    app = details['labels']['app']
    job_uuid = details['labels']['job_uuid']
    job_name = details['labels']['job_name']
    restart_count = payload.get('restart_count', 0)
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

    max_restarts = build_job.max_restarts or conf.get(MAX_RESTARTS_BUILD_JOBS)
    if JobLifeCycle.failed(payload['status']) and restart_count < max_restarts:
        return

    # Set the new status
    try:
        RedisStatuses.set_status(job_uuid, payload['status'])
        set_node_scheduling(build_job, details['node_name'])
        build_job.set_status(status=payload['status'],
                             message=payload['message'],
                             traceback=payload.get('traceback'),
                             details=details)
    except IntegrityError:
        # Due to concurrency this could happen, we just retry it
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)


@workers.app.task(name=K8SEventsCeleryTasks.K8S_EVENTS_RECONCILE_BUILD_JOB_STATUSES,
                  ignore_result=True)
def k8s_events_reconcile_build_job_statuses(job_id, status, created_at) -> None:
    try:
        job = BuildJob.objects.get(id=job_id)
    except ExperimentJob.DoesNotExist:
        logger.debug('Job `%s` does not exist', job_id)
        return

    if job.is_done:
        return

    job.set_status(status=status,
                   message='Status was reconciled.',
                   created_at=created_at)
