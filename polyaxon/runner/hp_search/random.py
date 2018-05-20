from experiment_groups.utils import get_running_experiment_group
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import HPCeleryTasks, Intervals
from runner.hp_search import base


def create(experiment_group):
    base.create_group_experiments(experiment_group=experiment_group)

    hp_random_search_start.apply_async((experiment_group.id,), countdown=1)


@celery_app.task(name=HPCeleryTasks.HP_RANDOM_SEARCH_CREATE)
def hp_random_search_create(experiment_group_id):
    experiment_group = get_running_experiment_group(experiment_group_id=experiment_group_id)
    if not experiment_group:
        return

    create(experiment_group)


@celery_app.task(name=HPCeleryTasks.HP_RANDOM_SEARCH_START, bind=True, max_retries=None)
def hp_random_search_start(self, experiment_group_id):
    experiment_group = get_running_experiment_group(experiment_group_id=experiment_group_id)
    if not experiment_group:
        return

    should_retry = base.start_group_experiments(experiment_group=experiment_group)
    if should_retry:
        # Schedule another task
        self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)
        return

    base.check_group_experiments_finished(experiment_group_id)
