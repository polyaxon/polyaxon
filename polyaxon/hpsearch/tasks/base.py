from db.models.experiments import Experiment
from hpsearch.tasks.logger import logger
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks


def get_suggestions(experiment_group):
    # Parse polyaxonfile content and create the experiments
    specification = experiment_group.specification
    suggestions = experiment_group.get_suggestions()

    if not suggestions:
        logger.error('Search algorithm `%s` could not make any suggestions.',
                     specification.search_algorithm,
                     extra={'stack': True})
        return

    return suggestions


def create_group_experiments(experiment_group, suggestions):
    # Parse polyaxonfile content and create the experiments
    specification = experiment_group.specification

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
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_GROUP_STOP_EXPERIMENTS,
            kwargs={'experiment_group_id': experiment_group.id,
                    'pending': True,
                    'message': 'Early stopping'})
        return

    experiment_to_start = experiment_group.n_experiments_to_start
    if experiment_to_start <= 0:
        # This could happen due to concurrency or not created yet experiments
        return (experiment_group.pending_experiments.exists() or
                not experiment_group.scheduled_all_suggestions())
    pending_experiments = experiment_group.pending_experiments[:experiment_to_start]
    n_pending_experiment = experiment_group.pending_experiments.count()

    for experiment in pending_experiments:
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_BUILD,
            kwargs={'experiment_id': experiment.id})

    return (n_pending_experiment - experiment_to_start > 0 or
            not experiment_group.scheduled_all_suggestions())


def check_group_experiments_finished(experiment_group_id, auto_retry=False):
    celery_app.send_task(SchedulerCeleryTasks.EXPERIMENTS_GROUP_CHECK_FINISHED,
                         kwargs={'experiment_group_id': experiment_group_id,
                                 'auto_retry': auto_retry})
