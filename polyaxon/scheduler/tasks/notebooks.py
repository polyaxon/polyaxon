import logging

import auditor
from constants.jobs import JobLifeCycle
from db.getters.projects import get_valid_project
from db.models.build_jobs import BuildJob
from docker_images.image_info import get_notebook_image_info
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks

from event_manager.events.build_job import BUILD_JOB_STARTED_TRIGGERED
from scheduler import dockerizer_scheduler, notebook_scheduler

_logger = logging.getLogger(__name__)


@celery_app.task(name=SchedulerCeleryTasks.PROJECTS_NOTEBOOK_BUILD, ignore_result=True)
def projects_notebook_build(project_id):
    project = get_valid_project(project_id=project_id)
    if not project or not project.notebook:
        _logger.warning('Project does not have a notebook.')
        return None

    job = project.notebook

    build_job = BuildJob.create(
        user=job.user,
        project=job.project,
        config=job.specification.run_exec,
        code_reference=job.code_reference)

    if dockerizer_scheduler.check_image(build_job=build_job):
        # The image already exists, so we can start the experiment right away
        celery_app.send_task(
            SchedulerCeleryTasks.PROJECTS_NOTEBOOK_START,
            kwargs={'project_id': project_id})
        return

    # We need to build the image first
    auditor.record(event_type=BUILD_JOB_STARTED_TRIGGERED,
                   instance=build_job,
                   target='project',
                   actor_id=job.user.id)
    build_status = dockerizer_scheduler.start_dockerizer(build_job=build_job)

    if not build_status:
        job.set_status(JobLifeCycle.FAILED, message='Could not start build process.')
        return

    if not JobLifeCycle.can_transition(status_from=job.last_status,
                                       status_to=JobLifeCycle.BUILDING):
        _logger.info('Notebook for project id `%s` cannot transition from `%s` to `%s`.',
                     project_id, job.last_status, JobLifeCycle.BUILDING)
        return

    # Update job status to show that its building docker image
    job.set_status(JobLifeCycle.BUILDING, message='Building container')


@celery_app.task(name=SchedulerCeleryTasks.PROJECTS_NOTEBOOK_START, ignore_result=True)
def projects_notebook_start(project_id):
    project = get_valid_project(project_id=project_id)
    if not project or not project.notebook:
        _logger.warning('Project does not have a notebook.')
        return None

    if project.notebook.last_status == JobLifeCycle.RUNNING:
        _logger.warning('Tensorboard is already running.')
        return None

    try:
        image_name, image_tag = get_notebook_image_info(project=project, job=project.notebook)
    except ValueError as e:
        _logger.warning('Could not start the notebook, %s', e)
        return
    job_docker_image = '{}:{}'.format(image_name, image_tag)
    _logger.info('Start notebook with built image `%s`', job_docker_image)

    notebook_scheduler.start_notebook(project.notebook, image=job_docker_image)


@celery_app.task(name=SchedulerCeleryTasks.PROJECTS_NOTEBOOK_STOP, ignore_result=True)
def projects_notebook_stop(project_id):
    project = get_valid_project(project_id=project_id)
    if not project:
        return None

    notebook_scheduler.stop_notebook(project.notebook, update_status=True)
