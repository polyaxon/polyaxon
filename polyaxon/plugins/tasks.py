import logging

from docker.errors import DockerException

from constants.jobs import JobLifeCycle
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import RunnerCeleryTasks
from projects.utils import get_valid_project
from db.models.repos import Repo
from runner.dockerizer.builders import notebooks as notebooks_builder
from runner.dockerizer.images import get_notebook_image_info
from runner.schedulers import notebook_scheduler, tensorboard_scheduler

logger = logging.getLogger('polyaxon.tasks.projects')


@celery_app.task(name=RunnerCeleryTasks.PROJECTS_TENSORBOARD_START, ignore_result=True)
def start_tensorboard(project_id):
    project = get_valid_project(project_id)
    if not project or not project.tensorboard:
        logger.warning('Project does not have a tensorboard.')
        return None

    if project.tensorboard.last_status == JobLifeCycle.RUNNING:
        logger.warning('Tensorboard is already running.')
        return None
    tensorboard_scheduler.start_tensorboard(project)


@celery_app.task(name=RunnerCeleryTasks.PROJECTS_TENSORBOARD_STOP, ignore_result=True)
def stop_tensorboard(project_id):
    project = get_valid_project(project_id)
    if not project:
        return None
    tensorboard_scheduler.stop_tensorboard(project, update_status=True)


@celery_app.task(name=RunnerCeleryTasks.PROJECTS_NOTEBOOK_BUILD, ignore_result=True)
def build_notebook(project_id):
    project = get_valid_project(project_id)
    if not project or not project.notebook:
        return None

    job = project.notebook

    # Update job status to show that its building docker image
    job.set_status(JobLifeCycle.BUILDING, message='Building container')

    # Building the docker image
    try:
        status = notebooks_builder.build_notebook_job(project=project, job=project.notebook)
    except DockerException as e:
        logger.warning('Failed to build notebook %s', e)
        job.set_status(
            JobLifeCycle.FAILED,
            message='Failed to build image for notebook.')
        return
    except Repo.DoesNotExist:
        logger.warning('No code was found for this project')
        job.set_status(
            JobLifeCycle.FAILED,
            message='Failed to build image for notebook.')
        return
    except Exception as e:  # Other exceptions
        logger.warning('Failed to build notebook %s', e)
        job.set_status(JobLifeCycle.FAILED,
                       message='Failed to build image for notebook.')
        return

    if not status:
        return

    # Now we can start the notebook
    start_notebook.delay(project_id=project_id)


@celery_app.task(name=RunnerCeleryTasks.PROJECTS_NOTEBOOK_START, ignore_result=True)
def start_notebook(project_id):
    project = get_valid_project(project_id)
    if not project or not project.notebook:
        logger.warning('Project does not have a notebook.')
        return None

    if project.notebook.last_status == JobLifeCycle.RUNNING:
        logger.warning('Tensorboard is already running.')
        return None

    try:
        image_name, image_tag = get_notebook_image_info(project=project, job=project.notebook)
    except ValueError as e:
        logger.warning('Could not start the notebook, %s', e)
        return
    job_docker_image = '{}:{}'.format(image_name, image_tag)
    logger.info('Start notebook with built image `%s`', job_docker_image)

    notebook_scheduler.start_notebook(project, image=job_docker_image)


@celery_app.task(name=RunnerCeleryTasks.PROJECTS_NOTEBOOK_STOP, ignore_result=True)
def stop_notebook(project_id):
    project = get_valid_project(project_id)
    if not project:
        return None

    notebook_scheduler.stop_notebook(project, update_status=True)
