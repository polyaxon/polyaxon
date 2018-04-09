import logging

from docker.errors import DockerException

from dockerizer.builders import notebooks as notebooks_builder
from dockerizer.images import get_notebook_image_info
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import CeleryTasks
from projects.models import Project
from repos.models import Repo
from schedulers import notebook_scheduler, tensorboard_scheduler
from spawners.utils.constants import JobLifeCycle

logger = logging.getLogger('polyaxon.tasks.projects')


def get_valid_project(project_id):
    try:
        return Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        logger.info('Project id `%s` does not exist', project_id)
        return None


@celery_app.task(name=CeleryTasks.PROJECTS_TENSORBOARD_START, ignore_result=True)
def start_tensorboard(project_id):
    project = get_valid_project(project_id)
    if not project or not project.tensorboard or project.has_tensorboard:
        return None
    tensorboard_scheduler.start_tensorboard(project)


@celery_app.task(name=CeleryTasks.PROJECTS_TENSORBOARD_STOP, ignore_result=True)
def stop_tensorboard(project_id):
    project = get_valid_project(project_id)
    if not project:
        return None
    tensorboard_scheduler.stop_tensorboard(project, update_status=True)


@celery_app.task(name=CeleryTasks.PROJECTS_NOTEBOOK_BUILD, ignore_result=True)
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

    if not status:
        return

    # Now we can start the notebook
    start_notebook.delay(project_id=project_id)


@celery_app.task(name=CeleryTasks.PROJECTS_NOTEBOOK_START, ignore_result=True)
def start_notebook(project_id):
    project = get_valid_project(project_id)
    if not project or not project.notebook or project.has_notebook:
        return None

    try:
        image_name, image_tag = get_notebook_image_info(project=project, job=project.notebook)
    except ValueError as e:
        logger.warning('Could not start the notebook, %s', e)
        return
    job_docker_image = '{}:{}'.format(image_name, image_tag)
    logger.info('Start notebook with built image `%s`', job_docker_image)

    notebook_scheduler.start_notebook(project, image=job_docker_image)


@celery_app.task(name=CeleryTasks.PROJECTS_NOTEBOOK_STOP, ignore_result=True)
def stop_notebook(project_id):
    project = get_valid_project(project_id)
    if not project:
        return None

    notebook_scheduler.stop_notebook(project, update_status=True)
