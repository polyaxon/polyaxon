import logging

from constants.jobs import JobLifeCycle
from db.getters.projects import get_valid_project
from docker_images.image_info import get_notebook_image_info
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks
from scheduler import notebook_scheduler

_logger = logging.getLogger(__name__)


@celery_app.task(name=SchedulerCeleryTasks.PROJECTS_NOTEBOOK_BUILD, ignore_result=True)
def projects_notebook_build(project_id):
    project = get_valid_project(project_id=project_id)
    if not project or not project.notebook:
        _logger.warning('Project does not have a notebook.')
        return None


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
