import logging

from django.conf import settings
from django.db import IntegrityError

from experiments.models import Experiment, ExperimentJob
from experiments.paths import get_experiment_logs_path
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import RunnerCeleryTasks
from models.projects import Project
from runner.nodes.models import ClusterEvent

logger = logging.getLogger('polyaxon.tasks.event_monitors')


@celery_app.task(name=RunnerCeleryTasks.EVENTS_HANDLE_NAMESPACE)
def handle_events_namespace(cluster_id, payload):
    logger.info('handling events namespace for cluster: %s', cluster_id)
    ClusterEvent.objects.create(cluster_id=cluster_id, **payload)


@celery_app.task(name=RunnerCeleryTasks.EVENTS_HANDLE_RESOURCES)
def handle_events_resources(payload, persist):
    # here we must persist resources if requested
    logger.info('handling events resources with persist:%s', persist)
    logger.info(payload)


@celery_app.task(name=RunnerCeleryTasks.EVENTS_HANDLE_JOB_STATUSES)
def handle_events_job_statuses(payload):
    """Experiment jobs statuses"""
    details = payload['details']
    job_uuid = details['labels']['job_uuid']
    logger.debug('handling events status for job_uuid: %s', job_uuid)

    try:
        job = ExperimentJob.objects.get(uuid=job_uuid)
    except ExperimentJob.DoesNotExist:
        logger.info('Job uuid`%s` does not exist', job_uuid)
        return

    # Set the new status
    try:
        job.set_status(status=payload['status'], message=payload['message'], details=details)
    except IntegrityError:
        # Due to concurrency this could happen, we just ignore it
        pass


@celery_app.task(name=RunnerCeleryTasks.EVENTS_HANDLE_PLUGIN_JOB_STATUSES)
def handle_events_plugin_job_statuses(payload):
    """Project Plugin jobs statuses"""
    details = payload['details']
    app = details['labels']['app']
    project_uuid = details['labels']['project_uuid']
    project_name = details['labels']['project_name']
    logger.debug('handling events status for project %s %s', project_name, app)

    try:
        project = Project.objects.get(uuid=project_uuid)
        if app == settings.APP_LABELS_TENSORBOARD:
            job = project.tensorboard
        elif app == settings.APP_LABELS_NOTEBOOK:
            job = project.notebook
        else:
            logger.info('Plugin job `%s` does not exist', app)
            return
        if job is None:
            logger.info('Project `%s` Job `%s` does not exist', project_name, app)
            return
    except Project.DoesNotExist:
        logger.info('Project `%s` does not exist', project_name)
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
    logger.debug('handling log event for %s %s', experiment_uuid, job_uuid)
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
