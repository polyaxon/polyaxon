from db.getters.experiment_groups import get_running_experiment_group
from hpsearch.tasks import base
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import HPCeleryTasks, Intervals


def create(experiment_group):
    experiments = base.create_group_experiments(experiment_group=experiment_group)
    experiment_ids = [xp.id for xp in experiments]
    experiments_configs = [[xp.id, xp.declarations] for xp in experiments]
    experiment_group.iteration_manager.create_iteration(
        experiment_ids=experiment_ids,
        experiments_configs=experiments_configs)
    hp_bo_start.apply_async((experiment_group.id,), countdown=1)


@celery_app.task(name=HPCeleryTasks.HP_BO_CREATE)
def hp_bo_create(experiment_group_id):
    experiment_group = get_running_experiment_group(experiment_group_id=experiment_group_id)
    if not experiment_group:
        return

    create(experiment_group)


@celery_app.task(name=HPCeleryTasks.HP_BO_START, bind=True, max_retries=None)
def hp_bo_start(self, experiment_group_id):
    experiment_group = get_running_experiment_group(experiment_group_id=experiment_group_id)
    if not experiment_group:
        return

    should_retry = base.start_group_experiments(experiment_group=experiment_group)
    if should_retry:
        # Schedule another task
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)
        return

    hp_bo_iterate.delay(experiment_group_id=experiment_group_id)


@celery_app.task(name=HPCeleryTasks.HP_BO_ITERATE, bind=True, max_retries=None)
def hp_bo_iterate(self, experiment_group_id):
    experiment_group = get_running_experiment_group(experiment_group_id=experiment_group_id)
    if not experiment_group:
        return

    if experiment_group.non_done_experiments.count() > 0:
        # Schedule another task, because all experiment must be done
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)
        return

    iteration_config = experiment_group.iteration_config
    iteration_manager = experiment_group.iteration_manager
    search_manager = experiment_group.search_manager

    iteration_manager.update_iteration()

    if search_manager.should_reschedule(iteration=iteration_config.iteration):
        hp_bo_create.delay(experiment_group_id=experiment_group_id)
        return

    base.check_group_experiments_finished(experiment_group_id)
