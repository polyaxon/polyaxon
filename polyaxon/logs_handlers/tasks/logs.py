import publisher

from db.models.build_jobs import BuildJob
from db.models.experiments import Experiment
from db.models.jobs import Job
from logs_handlers.tasks.logger import logger
from logs_handlers.utils import safe_log_experiment_job, safe_log_job
from polyaxon.celery_api import celery_app
from polyaxon.settings import LogsCeleryTasks


def handle_experiment_job_log(experiment_name,
                              experiment_uuid,
                              log_lines):
    if not Experiment.objects.filter(uuid=experiment_uuid).exists():
        return

    logger.debug('handling log event for %s', experiment_uuid)
    safe_log_experiment_job(experiment_name=experiment_name, log_lines=log_lines)


@celery_app.task(name=LogsCeleryTasks.LOGS_SIDECARS_EXPERIMENTS, ignore_result=True)
def logs_sidecars_experiments(experiment_name, experiment_uuid, job_uuid, log_lines):
    """Signal handling for sidecars logs."""
    handle_experiment_job_log(experiment_name=experiment_name,
                              experiment_uuid=experiment_uuid,
                              log_lines=log_lines)
    publisher.publish_experiment_job_log(
        log_lines=log_lines,
        experiment_uuid=experiment_uuid,
        experiment_name=experiment_name,
        job_uuid=job_uuid,
        send_task=False
    )


@celery_app.task(name=LogsCeleryTasks.LOGS_HANDLE_EXPERIMENT_JOB, ignore_result=True)
def logs_handle_experiment_job(experiment_name, experiment_uuid, log_lines):
    """Task handling for sidecars logs."""
    handle_experiment_job_log(experiment_name=experiment_name,
                              experiment_uuid=experiment_uuid,
                              log_lines=log_lines)


def handle_job_logs(job_uuid, job_name, log_lines):
    if not Job.objects.filter(uuid=job_uuid).exists():
        return

    logger.debug('handling log event for %s', job_name)
    safe_log_job(job_name=job_name, log_lines=log_lines)


@celery_app.task(name=LogsCeleryTasks.LOGS_SIDECARS_JOBS, ignore_result=True)
def logs_sidecars_jobs(job_uuid, job_name, log_lines):
    """Signal handling for sidecars logs."""
    handle_job_logs(job_uuid=job_uuid,
                    job_name=job_name,
                    log_lines=log_lines)
    publisher.publish_job_log(
        log_lines=log_lines,
        job_uuid=job_uuid,
        job_name=job_name,
        send_task=False
    )


@celery_app.task(name=LogsCeleryTasks.LOGS_HANDLE_JOB, ignore_result=True)
def logs_handle_job(job_uuid, job_name, log_lines):
    """Task handling for sidecars logs."""
    handle_job_logs(job_uuid=job_uuid,
                    job_name=job_name,
                    log_lines=log_lines)


def handle_build_job_logs(job_uuid, job_name, log_lines):
    if not BuildJob.objects.filter(uuid=job_uuid).exists():
        return

    logger.debug('handling log event for %s', job_name)
    safe_log_job(job_name=job_name, log_lines=log_lines)


@celery_app.task(name=LogsCeleryTasks.LOGS_SIDECARS_BUILDS, ignore_result=True)
def logs_sidecars_builds(job_uuid, job_name, log_lines):
    """Signal handling for sidecars logs."""
    handle_build_job_logs(job_uuid=job_uuid,
                          job_name=job_name,
                          log_lines=log_lines)
    publisher.publish_build_job_log(
        log_lines=log_lines,
        job_uuid=job_uuid,
        job_name=job_name,
        send_task=False
    )


@celery_app.task(name=LogsCeleryTasks.LOGS_HANDLE_BUILD_JOB, ignore_result=True)
def logs_handle_build_job(job_uuid, job_name, log_lines):
    """Task handling for sidecars logs."""
    handle_build_job_logs(job_uuid=job_uuid,
                          job_name=job_name,
                          log_lines=log_lines)
