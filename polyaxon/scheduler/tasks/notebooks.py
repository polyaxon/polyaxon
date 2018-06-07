import logging

from constants.jobs import JobLifeCycle
from db.getters.notebooks import get_valid_notebook
from docker_images.image_info import get_image_info
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks
from scheduler import dockerizer_scheduler, notebook_scheduler

_logger = logging.getLogger(__name__)


@celery_app.task(name=SchedulerCeleryTasks.PROJECTS_NOTEBOOK_BUILD, ignore_result=True)
def projects_notebook_build(notebook_job_id):
    notebook_job = get_valid_notebook(notebook_job_id=notebook_job_id)
    if notebook_job:
        _logger.warning('Notebook does not exist anymore.')
        return None

    if not JobLifeCycle.can_transition(status_from=notebook_job.last_status,
                                       status_to=JobLifeCycle.BUILDING):
        _logger.info('Notebook `%s` cannot transition from `%s` to `%s`.',
                     notebook_job, notebook_job.last_status, JobLifeCycle.BUILDING)
        return

    build_job, image_exists, build_status = dockerizer_scheduler.create_build_job(
        user=notebook_job.user,
        project=notebook_job.project,
        config=notebook_job.specification.build,
        code_reference=notebook_job.code_reference)

    notebook_job.build_job = build_job
    notebook_job.save()
    if image_exists:
        # The image already exists, so we can start the experiment right away
        celery_app.send_task(
            SchedulerCeleryTasks.PROJECTS_NOTEBOOK_START,
            kwargs={'notebook_job_id': notebook_job_id})
        return

    if not build_status:
        notebook_job.set_status(JobLifeCycle.FAILED, message='Could not start build process.')
        return

    # Update job status to show that its building docker image
    notebook_job.set_status(JobLifeCycle.BUILDING, message='Building container')


@celery_app.task(name=SchedulerCeleryTasks.PROJECTS_NOTEBOOK_START, ignore_result=True)
def projects_notebook_start(notebook_job_id):
    notebook_job = get_valid_notebook(notebook_job_id=notebook_job_id)
    if not notebook_job:
        _logger.warning('Notebook does not exist anymore.')
        return None

    if notebook_job.last_status == JobLifeCycle.RUNNING:
        _logger.warning('Notebook is already running.')
        return None

    try:
        image_name, image_tag = get_image_info(build_job=notebook_job.build_job)
    except ValueError as e:
        _logger.warning('Could not start the notebook, %s', e)
        return
    job_docker_image = '{}:{}'.format(image_name, image_tag)
    _logger.info('Start notebook with built image `%s`', job_docker_image)

    notebook_scheduler.start_notebook(notebook_job, image=job_docker_image)


@celery_app.task(name=SchedulerCeleryTasks.PROJECTS_NOTEBOOK_STOP, ignore_result=True)
def projects_notebook_stop(notebook_job_id):
    notebook = get_valid_notebook(notebook_job_id=notebook_job_id)
    if not notebook:
        return None

    notebook_scheduler.stop_notebook(notebook, update_status=True)
