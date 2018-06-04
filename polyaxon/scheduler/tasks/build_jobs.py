import logging

from db.getters.build_jobs import get_valid_build_job
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks
from scheduler import dockerizer_scheduler

_logger = logging.getLogger('polyaxon.scheduler.build_jobs')


@celery_app.task(name=SchedulerCeleryTasks.BUILD_JOBS_START, ignore_result=True)
def experiments_start(build_job_id):
    build_job = get_valid_build_job(build_job_id=build_job_id)
    if not build_job:
        _logger.info('Something went wrong, '
                     'the BuildJob `%s` does not exist anymore.', build_job_id)
        return

    dockerizer_scheduler.start_dockerizer(build_job)


@celery_app.task(name=SchedulerCeleryTasks.BUILD_JOBS_STOP, ignore_result=True)
def experiments_stop(build_job_id, update_status=True):
    build_job = get_valid_build_job(build_job_id=build_job_id)
    if not build_job:
        _logger.info('Something went wrong, '
                     'the BuildJob `%s` does not exist anymore.', build_job_id)
        return

    dockerizer_scheduler.stop_dockerizer(build_job, update_status=update_status)
