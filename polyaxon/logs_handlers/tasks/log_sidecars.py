from typing import Iterable, Optional, Union

import publisher

from logs_handlers.handlers import handle_build_job_logs, handle_experiment_job_log, handle_job_logs
from polyaxon.celery_api import celery_app
from polyaxon.settings import LogsCeleryTasks


@celery_app.task(name=LogsCeleryTasks.LOGS_SIDECARS_EXPERIMENTS, ignore_result=True)
def logs_sidecars_experiments(experiment_name: str,
                              experiment_uuid: str,
                              job_uuid: str,
                              log_lines: Optional[Union[str, Iterable[str]]]) -> None:
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


@celery_app.task(name=LogsCeleryTasks.LOGS_SIDECARS_JOBS, ignore_result=True)
def logs_sidecars_jobs(job_uuid: str,
                       job_name: str,
                       log_lines: Optional[Union[str, Iterable[str]]]) -> None:
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


@celery_app.task(name=LogsCeleryTasks.LOGS_SIDECARS_BUILDS, ignore_result=True)
def logs_sidecars_builds(job_uuid: str,
                         job_name: str,
                         log_lines: Optional[Union[str, Iterable[str]]]) -> None:
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
