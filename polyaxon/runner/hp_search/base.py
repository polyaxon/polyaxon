import logging

from experiments.models import Experiment
from runner.tasks.experiments import build_experiment

logger = logging.getLogger('polyaxon.runner.hp_search')


def create_group_experiments(experiment_group):
    # Parse polyaxonfile content and create the experiments
    specification = experiment_group.specification
    suggestions = experiment_group.get_suggestions()

    if not suggestions:
        logger.warning('Search algorithm was not found `%s`', specification.search_algorithm)
        return

    experiments = []
    for suggestion in suggestions:
        # We need to check if we should create or restart
        experiment = Experiment.objects.create(
            project_id=experiment_group.project_id,
            user_id=experiment_group.user_id,
            experiment_group=experiment_group,
            config=specification.get_experiment_spec(matrix_declaration=suggestion).parsed_data,
            code_reference_id=experiment_group.code_reference_id)
        experiments.append(experiment)

    return experiments


def start_group_experiments(experiment_group):
    # Check for early stopping before starting new experiments from this group
    if experiment_group.should_stop_early():
        from runner.tasks.experiment_groups import stop_group_experiments

        stop_group_experiments(experiment_group_id=experiment_group.id,
                               pending=True,
                               message='Early stopping')
        return

    experiment_to_start = experiment_group.n_experiments_to_start
    pending_experiments = experiment_group.pending_experiments[:experiment_to_start]
    n_pending_experiment = experiment_group.pending_experiments.count()

    for experiment in pending_experiments:
        build_experiment.delay(experiment_id=experiment.id)

    return n_pending_experiment - experiment_to_start > 0
