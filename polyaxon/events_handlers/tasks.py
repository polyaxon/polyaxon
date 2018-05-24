import logging

from django.conf import settings
from django.db import IntegrityError

from db.models.experiments import Experiment, ExperimentJob
from libs.paths.experiments import get_experiment_logs_path
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import RunnerCeleryTasks
from db.models.projects import Project
from db.models.nodes import ClusterEvent

_logger = logging.getLogger(__name__)


@celery_app.task(name=RunnerCeleryTasks.EVENTS_HANDLE_NAMESPACE)
def handle_events_namespace(cluster_id, payload):
    _logger.info('handling events namespace for cluster: %s', cluster_id)
    ClusterEvent.objects.create(cluster_id=cluster_id, **payload)


@celery_app.task(name=RunnerCeleryTasks.EVENTS_HANDLE_RESOURCES)
def handle_events_resources(payload, persist):
    # here we must persist resources if requested
    _logger.info('handling events resources with persist:%s', persist)
    _logger.info(payload)


@celery_app.task(name=RunnerCeleryTasks.EVENTS_HANDLE_JOB_STATUSES)
def handle_events_job_statuses(payload):
    """Experiment jobs constants"""
    details = payload['details']
    job_uuid = details['labels']['job_uuid']
    _logger.debug('handling events status for job_uuid: %s', job_uuid)

    try:
        job = ExperimentJob.objects.get(uuid=job_uuid)
    except ExperimentJob.DoesNotExist:
        _logger.info('Job uuid`%s` does not exist', job_uuid)
        return

    # Set the new status
    try:
        job.set_status(status=payload['status'], message=payload['message'], details=details)
    except IntegrityError:
        # Due to concurrency this could happen, we just ignore it
        pass


@celery_app.task(name=RunnerCeleryTasks.EVENTS_HANDLE_PLUGIN_JOB_STATUSES)
def handle_events_plugin_job_statuses(payload):
    """Project Plugin jobs constants"""
    details = payload['details']
    app = details['labels']['app']
    project_uuid = details['labels']['project_uuid']
    project_name = details['labels']['project_name']
    _logger.debug('handling events status for project %s %s', project_name, app)

    try:
        project = Project.objects.get(uuid=project_uuid)
        if app == settings.APP_LABELS_TENSORBOARD:
            job = project.tensorboard
        elif app == settings.APP_LABELS_NOTEBOOK:
            job = project.notebook
        else:
            _logger.info('Plugin job `%s` does not exist', app)
            return
        if job is None:
            _logger.info('Project `%s` Job `%s` does not exist', project_name, app)
            return
    except Project.DoesNotExist:
        _logger.info('Project `%s` does not exist', project_name)
        return

    # Set the new status
    try:
        job.set_status(status=payload['status'], message=payload['message'], details=details)
    except IntegrityError:
        # Due to concurrency this could happen, we just ignore it
        pass


@celery_app.task(name=RunnerCeleryTasks.EVENTS_HANDLE_LOGS_SIDECAR)
def handle_events_job_logs(experiment_name,
                           experiment_uuid,
                           job_uuid,
                           log_line,
                           task_type=None,
                           task_idx=None):
    # Must persist resources if logs according to the config
    if not Experiment.objects.filter(uuid=experiment_uuid).exists():
        return
    _logger.debug('handling log event for %s %s', experiment_uuid, job_uuid)
    if task_type and task_idx:
        log_line = '{}.{} -- {}'.format(task_type, int(task_idx) + 1, log_line)
    xp_logger = logging.getLogger(experiment_name)
    log_path = get_experiment_logs_path(experiment_name)
    try:
        log_handler = logging.FileHandler(log_path)
        log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        log_handler.setFormatter(log_formatter)
        xp_logger.addHandler(log_handler)
        xp_logger.setLevel(logging.INFO)
        xp_logger.info(log_line)
        xp_logger.handlers = []
    except OSError:
        # TODO: retry instead?
        pass
