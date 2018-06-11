import logging

from django.conf import settings
from django.db import IntegrityError

from db.models.build_jobs import BuildJob
from db.models.experiment_jobs import ExperimentJob
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.nodes import ClusterEvent
from db.models.notebooks import NotebookJob
from db.models.projects import Project
from db.models.tensorboards import TensorboardJob
from events_handlers.utils import safe_log_experiment_job, safe_log_job
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import EventsCeleryTasks

_logger = logging.getLogger(__name__)


@celery_app.task(name=EventsCeleryTasks.EVENTS_HANDLE_NAMESPACE)
def handle_events_namespace(cluster_id, payload):
    _logger.debug('handling events namespace for cluster: %s', cluster_id)
    ClusterEvent.objects.create(cluster_id=cluster_id, **payload)


@celery_app.task(name=EventsCeleryTasks.EVENTS_HANDLE_RESOURCES)
def handle_events_resources(payload, persist):
    # here we must persist resources if requested
    _logger.info('handling events resources with persist:%s', persist)
    _logger.info(payload)


@celery_app.task(name=EventsCeleryTasks.EVENTS_HANDLE_EXPERIMENT_JOB_STATUSES)
def events_handle_experiment_job_statuses(payload):
    """Experiment jobs statuses"""
    details = payload['details']
    job_uuid = details['labels']['job_uuid']
    _logger.debug('handling events status for job_uuid: %s', job_uuid)

    try:
        job = ExperimentJob.objects.get(uuid=job_uuid)
    except ExperimentJob.DoesNotExist:
        _logger.debug('Job uuid`%s` does not exist', job_uuid)
        return

    try:
        job.experiment
    except Experiment.DoesNotExist:
        _logger.debug('Experiment for job `%s` does not exist anymore', job_uuid)
        return

    # Set the new status
    try:
        job.set_status(status=payload['status'], message=payload['message'], details=details)
    except IntegrityError:
        # Due to concurrency this could happen, we just ignore it
        pass


@celery_app.task(name=EventsCeleryTasks.EVENTS_HANDLE_JOB_STATUSES)
def events_handle_job_statuses(payload):
    """Project jobs statuses"""
    details = payload['details']
    job_uuid = details['labels']['job_uuid']
    job_name = details['labels']['job_name']
    project_name = details['labels']['project_name']
    _logger.debug('handling events status for job %s', job_name)

    try:
        job = Job.objects.get(uuid=job_uuid)
    except Job.DoesNotExist:
        _logger.debug('Job `%s` does not exist', job_name)
        return

    try:
        job.project
    except Project.DoesNotExist:
        _logger.debug('Project for job `%s` does not exist', project_name)
        return

    # Set the new status
    try:
        job.set_status(status=payload['status'], message=payload['message'], details=details)
    except IntegrityError:
        # Due to concurrency this could happen, we just ignore it
        pass


@celery_app.task(name=EventsCeleryTasks.EVENTS_HANDLE_PLUGIN_JOB_STATUSES)
def events_handle_plugin_job_statuses(payload):
    """Project Plugin jobs statuses"""
    details = payload['details']
    app = details['labels']['app']
    job_uuid = details['labels']['job_uuid']
    job_name = details['labels']['job_name']
    project_name = details['labels']['project_name']
    _logger.debug('handling events status for job %s %s', job_name, app)

    try:
        if app == settings.APP_LABELS_TENSORBOARD:
            job = TensorboardJob.objects.get(uuid=job_uuid)
        elif app == settings.APP_LABELS_NOTEBOOK:
            job = NotebookJob.objects.get(uuid=job_uuid)
        else:
            _logger.info('Plugin job `%s` does not exist', app)
            return
    except (NotebookJob.DoesNotExist, TensorboardJob.DoesNotExist):
        _logger.debug('`%s - %s` does not exist', app, job_name)
        return

    try:
        job.project
    except Project.DoesNotExist:
        _logger.debug('`%s` does not exist anymore', project_name)

    # Set the new status
    try:
        job.set_status(status=payload['status'], message=payload['message'], details=details)
    except IntegrityError:
        # Due to concurrency this could happen, we just ignore it
        pass


@celery_app.task(name=EventsCeleryTasks.EVENTS_HANDLE_BUILD_JOB_STATUSES)
def events_handle_build_job_statuses(payload):
    """Project Plugin jobs statuses"""
    details = payload['details']
    app = details['labels']['app']
    job_uuid = details['labels']['job_uuid']
    job_name = details['labels']['job_name']
    project_name = details['labels']['project_name']
    _logger.debug('handling events status for build jon %s %s', job_name, app)

    try:
        build_job = BuildJob.objects.get(uuid=job_uuid)
    except BuildJob.DoesNotExist:
        _logger.info('Build job `%s` does not exist', job_name)
        return

    try:
        build_job.project
    except Project.DoesNotExist:
        _logger.debug('`%s` does not exist anymore', project_name)

    # Set the new status
    try:
        build_job.set_status(status=payload['status'], message=payload['message'], details=details)
    except IntegrityError:
        # Due to concurrency this could happen, we just ignore it
        pass


@celery_app.task(name=EventsCeleryTasks.EVENTS_HANDLE_LOGS_EXPERIMENT_JOB)
def events_handle_logs_experiment_job(experiment_name,
                                      experiment_uuid,
                                      job_uuid,
                                      log_lines,
                                      task_type=None,
                                      task_idx=None):
    if not Experiment.objects.filter(uuid=experiment_uuid).exists():
        return

    _logger.debug('handling log event for %s %s', experiment_uuid, job_uuid)
    if task_type and task_idx:
        log_lines = ['{}.{} -- {}'.format(task_type, int(task_idx) + 1, log_line)
                     for log_line in log_lines]

    safe_log_experiment_job(experiment_name=experiment_name, log_lines=log_lines)


@celery_app.task(name=EventsCeleryTasks.EVENTS_HANDLE_LOGS_JOB)
def events_handle_logs_job(job_uuid, job_name, log_lines):
    if not Job.objects.filter(uuid=job_uuid).exists():
        return

    _logger.debug('handling log event for %s', job_name)
    safe_log_job(job_name=job_name, log_lines=log_lines)


@celery_app.task(name=EventsCeleryTasks.EVENTS_HANDLE_LOGS_BUILD_JOB)
def events_handle_logs_build_job(job_uuid, job_name, log_lines):
    if not BuildJob.objects.filter(uuid=job_uuid).exists():
        return

    _logger.debug('handling log event for %s', job_name)
    safe_log_job(job_name=job_name, log_lines=log_lines)
