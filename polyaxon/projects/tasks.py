# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from random import shuffle

from docker.errors import DockerException
from polyaxon_schemas.utils import SEARCH_METHODS

from polyaxon.settings import CeleryTasks, Intervals
from polyaxon.celery_api import app as celery_app
from experiments.tasks import build_experiment
from projects.models import ExperimentGroup, Project
from dockerizer.builders import notebooks as notebooks_builder
from dockerizer.images import get_notebook_image_info
from repos.models import Repo
from spawner import scheduler
from spawner.utils.constants import JobLifeCycle

logger = logging.getLogger('polyaxon.tasks.projects')


@celery_app.task(name=CeleryTasks.EXPERIMENTS_START_GROUP, bind=True, max_retries=None)
def start_group_experiments(self, experiment_group_id):
    try:
        experiment_group = ExperimentGroup.objects.get(id=experiment_group_id)
    except ExperimentGroup.DoesNotExist:
        logger.info('ExperimentGroup `{}` was not found.'.format(experiment_group_id))
        if self.request.retries < 2:
            logger.info('Trying again for ExperimentGroup `{}`.'.format(experiment_group_id))
            self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)

        logger.info('Something went wrong, '
                    'the ExperimentGroup `{}` does not exist anymore.'.format(experiment_group_id))
        return

    pending_experiments = list(experiment_group.pending_experiments)
    experiment_to_start = experiment_group.n_experiments_to_start

    if experiment_group.search_method == SEARCH_METHODS.RANDOM:
        shuffle(pending_experiments)

    while experiment_to_start > 0 and pending_experiments:
        experiment = pending_experiments.pop()
        build_experiment.delay(experiment_id=experiment.id)
        experiment_to_start -= 1

    if pending_experiments:
        # Schedule another task
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)


def get_valid_project(project_id):
    try:
        return Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        logger.info('Project id `{}` does not exist'.format(project_id))
        return None


@celery_app.task(name=CeleryTasks.PROJECTS_TENSORBOARD_START, ignore_result=True)
def start_tensorboard(project_id):
    project = get_valid_project(project_id)
    if not project or not project.tensorboard or project.has_tensorboard:
        return None
    scheduler.start_tensorboard(project)


@celery_app.task(name=CeleryTasks.PROJECTS_TENSORBOARD_STOP, ignore_result=True)
def stop_tensorboard(project_id):
    project = get_valid_project(project_id)
    if not project:
        return None
    scheduler.stop_tensorboard(project, update_status=True)


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
            message='Failed to build image for notebook.'.format(project.unique_name))
        return
    except Repo.DoesNotExist:
        logger.warning('No code was found for this project')
        job.set_status(
            JobLifeCycle.FAILED,
            message='Failed to build image for notebook.'.format(project.unique_name))
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
    logger.info('Start notebook with built image `{}`'.format(job_docker_image))

    scheduler.start_notebook(project, image=job_docker_image)


@celery_app.task(name=CeleryTasks.PROJECTS_NOTEBOOK_STOP, ignore_result=True)
def stop_notebook(project_id):
    project = get_valid_project(project_id)
    if not project:
        return None

    scheduler.stop_notebook(project, update_status=True)
