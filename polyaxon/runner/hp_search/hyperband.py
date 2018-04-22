from experiment_groups.utils import get_valid_experiment_group
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import HPCeleryTasks, Intervals
from runner.hp_search import base


def create(experiment_group):
    experiment_group.iteration_manager.create_iteration()
    experiments = base.create_group_experiments(experiment_group=experiment_group)
    experiment_group.iteration_manager.add_iteration_experiments(
        experiment_ids=[xp.id for xp in experiments])
    hp_hyperband_start.apply_async((experiment_group.id,), countdown=1)


@celery_app.task(name=HPCeleryTasks.HP_HYPERBAND_CREATE)
def hp_hyperband_create(experiment_group_id):
    experiment_group = get_valid_experiment_group(experiment_group_id=experiment_group_id)
    if not experiment_group:
        return

    create(experiment_group)


@celery_app.task(name=HPCeleryTasks.HP_HYPERBAND_START, bind=True, max_retries=None)
def hp_hyperband_start(self, experiment_group_id):
    experiment_group = get_valid_experiment_group(experiment_group_id=experiment_group_id)
    if not experiment_group:
        return

    should_retry = base.start_group_experiments(experiment_group=experiment_group)
    if should_retry:
        # Schedule another task
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)

    hp_hyperband_iterate.delay(experiment_group_id=experiment_group_id)


@celery_app.task(name=HPCeleryTasks.HP_HYPERBAND_ITERATE, bind=True, max_retries=None)
def hp_hyperband_iterate(self, experiment_group_id):
    experiment_group = get_valid_experiment_group(experiment_group_id=experiment_group_id)
    if not experiment_group:
        return

    if experiment_group.non_done_experiments.count() > 0:
        # Schedule another task, because all experiment must be done
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)

    iteration_config = experiment_group.iteration_config
    iteration_manager = experiment_group.iteration_manager
    search_manager = experiment_group.search_manager

    iteration_manager.update_iteration()

    if search_manager.should_reschedule(iteration=iteration_config.iteration,
                                        bracket_iteration=iteration_config.bracket_iteration):
        hp_hyperband_create.delay(experiment_group_id=experiment_group_id)
        return

    if search_manager.should_reduce_configs(iteration=iteration_config.iteration,
                                            bracket_iteration=iteration_config.bracket_iteration):
        iteration_manager.reduce_configs()
        hp_hyperband_start.delay(experiment_group_id=experiment_group_id)
