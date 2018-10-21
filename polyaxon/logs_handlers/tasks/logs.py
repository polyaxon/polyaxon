from db.models.build_jobs import BuildJob
from db.models.experiments import Experiment
from db.models.jobs import Job
from logs_handlers.tasks.logger import logger
from logs_handlers.utils import safe_log_experiment_job, safe_log_job
from polyaxon.celery_api import celery_app
from polyaxon.settings import LogsCeleryTasks


@celery_app.task(name=LogsCeleryTasks.LOGS_HANDLE_EXPERIMENT_JOB, ignore_result=True)
def logs_handle_experiment_job(experiment_name,
                               experiment_uuid,
                               log_lines):
    if not Experiment.objects.filter(uuid=experiment_uuid).exists():
        return

    logger.debug('handling log event for %s', experiment_uuid)
    safe_log_experiment_job(experiment_name=experiment_name, log_lines=log_lines)


@celery_app.task(name=LogsCeleryTasks.LOGS_HANDLE_JOB, ignore_result=True)
def logs_handle_job(job_uuid, job_name, log_lines):
    if not Job.objects.filter(uuid=job_uuid).exists():
        return

    logger.debug('handling log event for %s', job_name)
    safe_log_job(job_name=job_name, log_lines=log_lines)


@celery_app.task(name=LogsCeleryTasks.LOGS_HANDLE_BUILD_JOB, ignore_result=True)
def logs_handle_build_job(job_uuid, job_name, log_lines):
    if not BuildJob.objects.filter(uuid=job_uuid).exists():
        return

    logger.debug('handling log event for %s', job_name)
    safe_log_job(job_name=job_name, log_lines=log_lines)
