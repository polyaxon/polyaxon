import conf

from constants.experiment_groups import ExperimentGroupLifeCycle
from db.getters.experiment_groups import get_running_experiment_group
from hpsearch.exceptions import ExperimentGroupException
from hpsearch.tasks import base
from hpsearch.tasks.logger import logger
from polyaxon.celery_api import celery_app
from polyaxon.settings import HPCeleryTasks, Intervals


def create(experiment_group):
    suggestions = base.get_suggestions(experiment_group=experiment_group)
    if not suggestions:
        logger.error('Experiment group `%s` could not create any suggestion.',
                     experiment_group.id)
        experiment_group.set_status(ExperimentGroupLifeCycle.FAILED,
                                    message='Experiment group could not create new suggestions.')
        return

    experiment_group.iteration_manager.create_iteration(num_suggestions=len(suggestions))

    def send_chunk():
        celery_app.send_task(
            HPCeleryTasks.HP_GRID_SEARCH_CREATE_EXPERIMENTS,
            kwargs={'experiment_group_id': experiment_group.id,
                    'suggestions': chunk_suggestions},
            countdown=1)

    chunk_suggestions = []
    for suggestion in suggestions:
        chunk_suggestions.append(suggestion)
        if len(chunk_suggestions) == conf.get('GROUP_CHUNKS'):
            send_chunk()
            chunk_suggestions = []

    if chunk_suggestions:
        send_chunk()

    celery_app.send_task(
        HPCeleryTasks.HP_GRID_SEARCH_START,
        kwargs={'experiment_group_id': experiment_group.id, 'auto_retry': True},
        countdown=1)


@celery_app.task(name=HPCeleryTasks.HP_GRID_SEARCH_CREATE_EXPERIMENTS, ignore_result=True)
def hp_grid_search_create_experiments(experiment_group_id, suggestions):
    experiment_group = get_running_experiment_group(experiment_group_id=experiment_group_id)
    if not experiment_group:
        return

    try:
        experiments = base.create_group_experiments(experiment_group=experiment_group,
                                                    suggestions=suggestions)
    except ExperimentGroupException:  # The experiments will be stopped
        return

    experiment_group.iteration_manager.add_iteration_experiments(
        experiment_ids=[xp.id for xp in experiments])

    celery_app.send_task(
        HPCeleryTasks.HP_GRID_SEARCH_START,
        kwargs={'experiment_group_id': experiment_group.id},
        countdown=1)


@celery_app.task(name=HPCeleryTasks.HP_GRID_SEARCH_CREATE, ignore_result=True)
def hp_grid_search_create(experiment_group_id):
    experiment_group = get_running_experiment_group(experiment_group_id=experiment_group_id)
    if not experiment_group:
        return

    create(experiment_group=experiment_group)


@celery_app.task(name=HPCeleryTasks.HP_GRID_SEARCH_START,
                 bind=True,
                 max_retries=None,
                 ignore_result=True)
def hp_grid_search_start(self, experiment_group_id, auto_retry=False):
    if not base.should_group_start(experiment_group_id=experiment_group_id,
                                   task=HPCeleryTasks.HP_GRID_SEARCH_START,
                                   auto_retry=auto_retry):
        return

    experiment_group = get_running_experiment_group(experiment_group_id=experiment_group_id)
    if not experiment_group:
        return

    should_retry = base.start_group_experiments(experiment_group=experiment_group)
    if should_retry:
        if auto_retry:
            # Schedule another task
            self.retry(countdown=Intervals.EXPERIMENTS_SCHEDULER)
        return

    base.check_group_experiments_finished(experiment_group_id, auto_retry=auto_retry)
