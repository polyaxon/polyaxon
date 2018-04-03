import logging

import random

from polyaxon_schemas.utils import SEARCH_METHODS

from experiments.models import Experiment
from experiments.tasks import build_experiment, stop_experiment
from experiment_groups.models import ExperimentGroup
from polyaxon.settings import CeleryTasks, Intervals
from polyaxon.celery_api import app as celery_app
from spawners.utils.constants import ExperimentLifeCycle

logger = logging.getLogger('polyaxon.tasks.experiment_groups')


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


@celery_app.task(name=CeleryTasks.EXPERIMENTS_GROUP_CREATE, bind=True, max_retries=None)
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


@celery_app.task(name=CeleryTasks.EXPERIMENTS_GROUP_START, bind=True, max_retries=None)
def start_group_experiments(self, experiment_group_id):
    experiment_group = _get_group_ro_retry(experiment_group_id=experiment_group_id, task=self)
    if not experiment_group:
        return

    # Check for early stopping before starting new experiments from this group
    if experiment_group.should_stop_early():
        stop_group_experiments(experiment_group_id=experiment_group_id,
                               pending=True,
                               message='Early stopping')
        return

    experiment_to_start = experiment_group.n_experiments_to_start
    pending_experiments = experiment_group.pending_experiments[:experiment_to_start]
    n_pending_experiment = experiment_group.pending_experiments.count()

    for experiment in pending_experiments:
        build_experiment.delay(experiment_id=experiment.id)

    if n_pending_experiment - experiment_to_start > 0:
        # Schedule another task
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)


@celery_app.task(name=CeleryTasks.EXPERIMENTS_GROUP_STOP_EXPERIMENTS)
def stop_group_experiments(experiment_group_id, pending, message=None):
    try:
        experiment_group = ExperimentGroup.objects.get(id=experiment_group_id)
    except ExperimentGroup.DoesNotExist:
        logger.info('ExperimentGroup `{}` was not found.'.format(experiment_group_id))
        return

    if pending:
        for experiment in experiment_group.pending_experiments:
            # Update experiment status to show that its stopped
            experiment.set_status(status=ExperimentLifeCycle.STOPPED, message=message)
    else:
        for experiment in experiment_group.experiments.exclude(
                experiment_status__status__in=ExperimentLifeCycle.DONE_STATUS).distinct():
            if experiment.is_running:
                stop_experiment.delay(experiment_id=experiment.id)
            else:
                # Update experiment status to show that its stopped
                experiment.set_status(status=ExperimentLifeCycle.STOPPED, message=message)
