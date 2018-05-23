import logging

from db.models.experiments import Experiment

logger = logging.getLogger('polyaxon.experiments.utils')


def get_valid_experiment(experiment_id=None, experiment_uuid=None):
    if not any([experiment_id, experiment_uuid]) or all([experiment_id, experiment_uuid]):
        raise ValueError('`get_valid_experiment` function expects an experiment id or uuid.')

    try:
        if experiment_uuid:
            experiment = Experiment.objects.get(uuid=experiment_uuid)
        else:
            experiment = Experiment.objects.get(id=experiment_id)
    except Experiment.DoesNotExist:
        logger.info('Experiment id `%s` does not exist', experiment_id)
        return None

    return experiment


def is_experiment_still_running(experiment_id=None, experiment_uuid=None):
    experiment = get_valid_experiment(experiment_id=experiment_id, experiment_uuid=experiment_uuid)

    if not experiment or not experiment.is_running:
        return False

    return True
