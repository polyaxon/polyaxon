import logging

from experiment_groups.utils import get_valid_experiment_group
from experiments.models import Experiment
from experiments.statuses import ExperimentLifeCycle
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import CeleryTasks, Intervals
from runner.tasks.experiments import build_experiment, stop_experiment

logger = logging.getLogger('polyaxon.tasks.experiment_groups')


def _get_group_or_retry(experiment_group_id, task):
    experiment_group = get_valid_experiment_group(experiment_group_id=experiment_group_id)
    if experiment_group:
        return experiment_group

    # We retry if experiment group does not exist
    if task.request.retries < 2:
        logger.info('Trying again for ExperimentGroup `%s`.', experiment_group_id)
        task.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)

    logger.info('Something went wrong, '
                'the ExperimentGroup `%s` does not exist anymore.', experiment_group_id)
    return None


@celery_app.task(name=CeleryTasks.EXPERIMENTS_GROUP_CREATE, bind=True, max_retries=None)
def create_group_experiments(self, experiment_group_id, iteration=0):
    experiment_group = _get_group_or_retry(experiment_group_id=experiment_group_id, task=self)
    if not experiment_group:
        return

    # Parse polyaxonfile content and create the experiments
    specification = experiment_group.specification
    suggestions = experiment_group.get_suggestions(iteration=iteration)

    if not suggestions:
        logger.warning('Search algorithm was not found `%s`', specification.search_algorithm)
        return

    for suggestion in suggestions:
        # We need to check if we should create or restart
        Experiment.objects.create(
            project=experiment_group.project,
            user=experiment_group.user,
            experiment_group=experiment_group,
            config=specification.get_experiment_spec(matrix_declaration=suggestion).parsed_data)

    start_group_experiments.apply_async((experiment_group.id,), countdown=1)


@celery_app.task(name=CeleryTasks.EXPERIMENTS_GROUP_START, bind=True, max_retries=None)
def start_group_experiments(self, experiment_group_id):
    experiment_group = _get_group_or_retry(experiment_group_id=experiment_group_id, task=self)
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

    elif experiment_group.should_reschedule():
        create_group_experiments.delay(experiment_group_id=experiment_group_id)

    # elif experiment_group.reduce_experiments_to_restart():
    #     # Schedule another task
    #     self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)


@celery_app.task(name=CeleryTasks.EXPERIMENTS_GROUP_STOP_EXPERIMENTS)
def stop_group_experiments(experiment_group_id, pending, message=None):
    experiment_group = get_valid_experiment_group(experiment_group_id=experiment_group_id)
    if not experiment_group:
        return

    if pending:
        for experiment in experiment_group.pending_experiments:
            # Update experiment status to show that its stopped
            experiment.set_status(status=ExperimentLifeCycle.STOPPED, message=message)
    else:
        experiments = experiment_group.experiments.exclude(
            experiment_status__status__in=ExperimentLifeCycle.DONE_STATUS).distinct()
        for experiment in experiments:
            if experiment.is_running:
                stop_experiment.delay(experiment_id=experiment.id)
            else:
                # Update experiment status to show that its stopped
                experiment.set_status(status=ExperimentLifeCycle.STOPPED, message=message)
