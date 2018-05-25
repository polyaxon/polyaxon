import logging

import publisher

from constants.experiments import ExperimentLifeCycle
from db.getters.experiments import get_valid_experiment
from db.models.experiments import ExperimentMetric
from libs.paths.experiments import copy_experiment_outputs, create_experiment_outputs_path
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks
from scheduler import experiment_scheduler

logger = logging.getLogger('polyaxon.scheduler.experiments')


def copy_experiment(experiment):
    """If experiment is a restart, we should resume from last check point"""
    try:
        publisher.publish_experiment_log(
            log_line='Copying outputs from experiment `{}` into experiment `{}`'.format(
                experiment.original_experiment.unique_name, experiment.unique_name
            ),
            status=ExperimentLifeCycle.BUILDING,
            experiment_uuid=experiment.uuid.hex,
            experiment_name=experiment.unique_name,
            job_uuid='all',
        )
        copy_experiment_outputs(experiment.original_experiment.unique_name, experiment.unique_name)

    except OSError:
        publisher.publish_experiment_log(
            log_line='Could not copy the outputs of experiment `{}` into experiment `{}`'.format(
                experiment.original_experiment.unique_name, experiment.unique_name
            ),
            status=ExperimentLifeCycle.BUILDING,
            experiment_uuid=experiment.uuid.hex,
            experiment_name=experiment.unique_name,
            job_uuid='all',
        )
        logger.warning(
            'Could not copy the outputs of experiment `%s` into experiment `%s`',
            experiment.original_experiment.unique_name, experiment.unique_name)


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_CHECK_STATUS, ignore_result=True)
def check_experiment_status(experiment_uuid):
    experiment = get_valid_experiment(experiment_uuid=experiment_uuid)
    if not experiment:
        return
    experiment.update_status()


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_SET_METRICS, ignore_result=True)
def set_metrics(experiment_uuid, metrics, created_at=None):
    experiment = get_valid_experiment(experiment_uuid=experiment_uuid)
    if not experiment:
        return

    kwargs = {}
    if created_at:
        kwargs['created_at'] = created_at
    ExperimentMetric.objects.create(experiment=experiment, values=metrics, **kwargs)


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_START, ignore_result=True)
def start_experiment(experiment_id):
    experiment = get_valid_experiment(experiment_id=experiment_id)
    if not experiment:
        logger.info('Something went wrong, '
                    'the Experiment `%s` does not exist anymore.', experiment_id)
        return

    if not ExperimentLifeCycle.can_transition(status_from=experiment.last_status,
                                              status_to=ExperimentLifeCycle.SCHEDULED):
        logger.info('Experiment id `%s` cannot transition from `%s` to `%s`.',
                    experiment_id, experiment.last_status, ExperimentLifeCycle.BUILDING)
        return None

    # Check if we need to copy an experiment
    if experiment.is_copy:
        copy_experiment(experiment)
    else:
        create_experiment_outputs_path(experiment.unique_name)

    experiment_scheduler.start_experiment(experiment)


@celery_app.task(name=SchedulerCeleryTasks.EXPERIMENTS_STOP, ignore_result=True)
def stop_experiment(experiment_id):
    experiment = get_valid_experiment(experiment_id=experiment_id)
    if not experiment:
        logger.info('Something went wrong, '
                    'the Experiment `%s` does not exist anymore.', experiment_id)
        return

    experiment_scheduler.stop_experiment(experiment, update_status=True)
