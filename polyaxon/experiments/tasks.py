# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from docker.errors import DockerException
from polyaxon_schemas.utils import TIME_ZONE

from polyaxon.celery_api import app as celery_app
from polyaxon.settings import CeleryTasks, Intervals
from repos import dockerize
from repos.models import Repo

from spawner import scheduler
from spawner.utils.constants import ExperimentLifeCycle
from experiments.models import Experiment, ExperimentMetric

logger = logging.getLogger('polyaxon.tasks.experiments')


def get_valid_experiment(experiment_id):
    try:
        experiment = Experiment.objects.get(id=experiment_id)
    except Experiment.DoesNotExist:
        logger.info('Experiment id `{}` does not exist'.format(experiment_id))
        return None

    if experiment.is_done:
        logger.info('Experiment id `{}` stopped with status `{}`.'.format(experiment_id,
                                                                          experiment.last_status))
        return None

    return experiment


@celery_app.task(name=CeleryTasks.EXPERIMENTS_BUILD, bind=True, max_retries=3)
def build_experiment(self, experiment_id):
    experiment = get_valid_experiment(experiment_id=experiment_id)
    if not experiment:
        if self.request.retries < 2:
            logger.info('Trying again for Experiment `{}`.'.format(experiment_id))
            self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)

        logger.info('Something went wrong, '
                    'the Experiment `{}` does not exist anymore.'.format(experiment_id))
        return

    # No need to build the image, start the experiment directly
    if not experiment.compiled_spec.run_exec:
        start_experiment.delay(experiment_id=experiment_id)
        return

    # Update experiment status to show that its building
    experiment.set_status(ExperimentLifeCycle.BUILDING)

    # docker image
    try:
        status = dockerize.build_experiment(experiment)
    except DockerException as e:
        logger.warning('Failed to build experiment %s\n' % e)
        experiment.set_status(ExperimentLifeCycle.FAILED)
        return
    except Repo.DoesNotExist:
        logger.warning('No code was found for this project')
        experiment.set_status(ExperimentLifeCycle.FAILED)
        return

    if not status:
        return

    # Now we can start the experiment
    start_experiment.delay(experiment_id=experiment_id)


@celery_app.task(name=CeleryTasks.EXPERIMENTS_START)
def start_experiment(experiment_id):
    experiment = get_valid_experiment(experiment_id=experiment_id)
    if not experiment:
        return

    scheduler.start_experiment(experiment)


@celery_app.task(name=CeleryTasks.EXPERIMENTS_STOP)
def stop_experiment(experiment_id):
    experiment = get_valid_experiment(experiment_id=experiment_id)
    if not experiment:
        return

    scheduler.stop_experiment(experiment, update_status=True)


@celery_app.task(name=CeleryTasks.EXPERIMENTS_CHECK_STATUS)
def check_experiment_status(experiment_uuid):
    experiment = Experiment.objects.get(uuid=experiment_uuid)
    experiment.update_status()


@celery_app.task(name=CeleryTasks.EXPERIMENTS_SET_METRICS)
def set_metrics(experiment_uuid, created_at, metrics):
    created_at = TIME_ZONE.localize(created_at)
    try:
        experiment = Experiment.objects.get(uuid=experiment_uuid)
    except Experiment.DoesNotExist:
        logger.info('Experiment uuid `{}` does not exist'.format(experiment_uuid))
        return None

    ExperimentMetric.objects.create(experiment=experiment, created_at=created_at, values=metrics)
