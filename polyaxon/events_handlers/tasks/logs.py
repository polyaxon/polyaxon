from db.models.build_jobs import BuildJob
from db.models.experiments import Experiment
from db.models.jobs import Job
from events_handlers.tasks.logger import logger
from events_handlers.utils import safe_log_experiment_job, safe_log_job
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import EventsCeleryTasks


@celery_app.task(name=EventsCeleryTasks.EVENTS_HANDLE_LOGS_EXPERIMENT_JOB, ignore_result=True)
def events_handle_logs_experiment_job(experiment_name,
                                      experiment_uuid,
                                      job_uuid,
                                      log_lines,
                                      task_type=None,
                                      task_idx=None):
    if not Experiment.objects.filter(uuid=experiment_uuid).exists():
        return

    logger.debug('handling log event for %s %s', experiment_uuid, job_uuid)
    if task_type and task_idx:
        log_lines = ['{}.{} -- {}'.format(task_type, int(task_idx) + 1, log_line)
                     for log_line in log_lines]

    safe_log_experiment_job(experiment_name=experiment_name, log_lines=log_lines)


@celery_app.task(name=EventsCeleryTasks.EVENTS_HANDLE_LOGS_JOB, ignore_result=True)
def events_handle_logs_job(job_uuid, job_name, log_lines):
    if not Job.objects.filter(uuid=job_uuid).exists():
        return

    logger.debug('handling log event for %s', job_name)
    safe_log_job(job_name=job_name, log_lines=log_lines)


@celery_app.task(name=EventsCeleryTasks.EVENTS_HANDLE_LOGS_BUILD_JOB, ignore_result=True)
def events_handle_logs_build_job(job_uuid, job_name, log_lines):
    if not BuildJob.objects.filter(uuid=job_uuid).exists():
        return

    logger.debug('handling log event for %s', job_name)
    safe_log_job(job_name=job_name, log_lines=log_lines)
