import logging

from polyaxon_schemas.polyaxonfile.specification import JobSpecification

from constants.jobs import JobLifeCycle
from db.getters.jobs import get_valid_job
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks
from scheduler import dockerizer_scheduler, job_scheduler

_logger = logging.getLogger(__name__)


@celery_app.task(name=SchedulerCeleryTasks.JOBS_BUILD, ignore_result=True)
def jobs_build(job_id):
    job = get_valid_job(job_id=job_id)
    if not job:
        _logger.warning('Job does not have a notebook.')
        return None

    if not JobLifeCycle.can_transition(status_from=job.last_status,
                                       status_to=JobLifeCycle.BUILDING):
        _logger.info('Job id `%s` cannot transition from `%s` to `%s`.',
                     job_id, job.last_status, JobLifeCycle.BUILDING)
        return

    build_job, image_exists, build_status = dockerizer_scheduler.create_build_job(
        user=job.user,
        project=job.project,
        config=job.specification.build,
        code_reference=job.code_reference)

    job.build_job = build_job
    job.save()
    if image_exists:
        # The image already exists, so we can start the experiment right away
        celery_app.send_task(
            SchedulerCeleryTasks.JOBS_START,
            kwargs={'job_id': job_id})
        return

    if not build_status:
        job.set_status(JobLifeCycle.FAILED, message='Could not start build process.')
        return

    # Update job status to show that its building docker image
    job.set_status(JobLifeCycle.BUILDING, message='Building container')


@celery_app.task(name=SchedulerCeleryTasks.JOBS_START, ignore_result=True)
def jobs_start(job_id):
    job = get_valid_job(job_id=job_id)
    if not job:
        _logger.warning('Job does not exist.')
        return None

    if job.last_status == JobLifeCycle.RUNNING:
        _logger.warning('Job is already running.')
        return None

    if not JobLifeCycle.can_transition(status_from=job.last_status,
                                       status_to=JobLifeCycle.SCHEDULED):
        _logger.info('Job `%s` cannot transition from `%s` to `%s`.',
                     job.unique_name, job.last_status, JobLifeCycle.SCHEDULED)
        return None

    job_scheduler.start_job(job)


@celery_app.task(name=SchedulerCeleryTasks.JOBS_STOP, ignore_result=True)
def jobs_stop(project_name, project_uuid, job_name, job_uuid, specification, update_status=True):
    specification = JobSpecification.read(specification)
    job_scheduler.stop_job(
        project_name=project_name,
        project_uuid=project_uuid,
        job_name=job_name,
        job_uuid=job_uuid,
        specification=specification)

    if not update_status:
        return

    job = get_valid_job(job_uuid=job_uuid)
    if not job:
        return None

    # Update notebook status to show that its stopped
    job.set_status(status=JobLifeCycle.STOPPED,
                   message='job was stopped')
