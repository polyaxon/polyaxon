from db.models.build_jobs import BuildJob
from db.models.experiments import Experiment
from db.models.jobs import Job
from logs_handlers.tasks.logger import logger
from logs_handlers.utils import safe_log_experiment, safe_log_job


def handle_experiment_job_log(experiment_name,
                              experiment_uuid,
                              log_lines,
                              temp=True):
    if not Experiment.objects.filter(uuid=experiment_uuid).exists():
        return

    logger.debug('handling log event for %s', experiment_uuid)
    safe_log_experiment(experiment_name=experiment_name,
                        log_lines=log_lines,
                        temp=temp,
                        append=True)


def handle_job_logs(job_uuid, job_name, log_lines, temp=True):
    if not Job.objects.filter(uuid=job_uuid).exists():
        return

    logger.debug('handling log event for %s', job_name)
    safe_log_job(job_name=job_name, log_lines=log_lines, temp=temp, append=True)


def handle_build_job_logs(job_uuid, job_name, log_lines, temp=True):
    if not BuildJob.objects.filter(uuid=job_uuid).exists():
        return

    logger.debug('handling log event for %s', job_name)
    safe_log_job(job_name=job_name, log_lines=log_lines, temp=temp, append=True)
