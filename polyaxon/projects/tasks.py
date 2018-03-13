# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

import random

from docker.errors import DockerException
from polyaxon_schemas.utils import SEARCH_METHODS

from experiments.models import Experiment
from polyaxon.settings import CeleryTasks, Intervals
from polyaxon.celery_api import app as celery_app
from experiments.tasks import build_experiment
from projects.models import ExperimentGroup, Project
from dockerizer.builders import notebooks as notebooks_builder
from dockerizer.images import get_notebook_image_info
from repos.models import Repo
from schedulers import notebook_scheduler, tensorboard_scheduler
from spawners.utils.constants import JobLifeCycle

logger = logging.getLogger('polyaxon.tasks.projects')


def _get_group_ro_retry(experiment_group_id, task):
    try:
        return ExperimentGroup.objects.get(id=experiment_group_id)
    except ExperimentGroup.DoesNotExist:
        logger.info('ExperimentGroup `{}` was not found.'.format(experiment_group_id))
        if task.request.retries < 2:
            logger.info('Trying again for ExperimentGroup `{}`.'.format(experiment_group_id))
            task.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)

        logger.info('Something went wrong, '
                    'the ExperimentGroup `{}` does not exist anymore.'.format(experiment_group_id))
        return None


@celery_app.task(name=CeleryTasks.EXPERIMENTS_CREATE_GROUP, bind=True, max_retries=None)
def create_group_experiments(self, experiment_group_id):
    experiment_group = _get_group_ro_retry(experiment_group_id=experiment_group_id, task=self)
    if not experiment_group:
        return

    # Parse polyaxonfile content and create the experiments
    specification = experiment_group.specification
    # We create a list of indices that we will explore
    if SEARCH_METHODS.is_sequential(specification.search_method):
        indices = range(specification.n_experiments or specification.matrix_space)
    elif SEARCH_METHODS.is_random(specification.search_method):
        sub_space = specification.n_experiments or specification.matrix_space
        indices = random.sample(range(specification.matrix_space), sub_space)
    else:
        logger.warning('Search method was not found `{}`'.format(specification.search_method))
        return
    for xp in indices:
        Experiment.objects.create(project=experiment_group.project,
                                  user=experiment_group.user,
                                  experiment_group=experiment_group,
                                  config=specification.parsed_data[xp])

    start_group_experiments.apply_async((experiment_group.id,), countdown=1)


@celery_app.task(name=CeleryTasks.EXPERIMENTS_START_GROUP, bind=True, max_retries=None)
def start_group_experiments(self, experiment_group_id):
    experiment_group = _get_group_ro_retry(experiment_group_id=experiment_group_id, task=self)
    if not experiment_group:
        return

    # Check for early stopping before starting new experiments from this group
    if experiment_group.should_stop_early():
        experiment_group.stop_pending_experiments(message='Early stopping')
        return

    experiment_to_start = experiment_group.n_experiments_to_start
    pending_experiments = experiment_group.pending_experiments[:experiment_to_start]
    n_pending_experiment = experiment_group.pending_experiments.count()

    for experiment in pending_experiments:
        build_experiment.delay(experiment_id=experiment.id)

    if n_pending_experiment - experiment_to_start > 0:
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

    notebook_scheduler.start_notebook(project, image=job_docker_image)


@celery_app.task(name=CeleryTasks.PROJECTS_NOTEBOOK_STOP, ignore_result=True)
def stop_notebook(project_id):
    project = get_valid_project(project_id)
    if not project:
        return None

    notebook_scheduler.stop_notebook(project, update_status=True)
