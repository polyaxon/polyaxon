# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from random import shuffle

from polyaxon_schemas.utils import SEARCH_METHODS

from polyaxon.settings import CeleryTasks, Intervals
from polyaxon.celery_api import app as celery_app
from experiments.tasks import build_experiment
from projects.models import ExperimentGroup, Project
from spawner import scheduler

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


@celery_app.task(name=CeleryTasks.PROJECTS_TENSORBOARD_START, ignore_result=True)
def start_tensorboard(project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        logger.info('Project id `{}` does not exist'.format(project_id))
        return None

    scheduler.start_tensorboard(project)


@celery_app.task(name=CeleryTasks.PROJECTS_TENSORBOARD_STOP, ignore_result=True)
def stop_tensorboard(project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        logger.info('Project id `{}` does not exist'.format(project_id))
        return None

    scheduler.stop_tensorboard(project)
