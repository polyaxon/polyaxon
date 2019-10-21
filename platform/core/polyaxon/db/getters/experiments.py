import logging

from db.models.experiments import Experiment

_logger = logging.getLogger('polyaxon.db')


def get_valid_experiment(experiment_id: int = None,
                         experiment_uuid: str = None,
                         include_deleted: bool = False):
    if not any([experiment_id, experiment_uuid]) or all([experiment_id, experiment_uuid]):
        raise ValueError('`get_valid_experiment` function expects an experiment id or uuid.')

    try:
        qs = Experiment.all if include_deleted else Experiment.objects
        if experiment_uuid:
            experiment = qs.get(uuid=experiment_uuid)
        else:
            experiment = qs.get(id=experiment_id)
    except Experiment.DoesNotExist:
        _logger.info('Experiment `%s` does not exist', experiment_id or experiment_uuid)
        return None

    return experiment


def is_experiment_still_running(experiment_id: int = None,
                                experiment_uuid: str = None):
    experiment = get_valid_experiment(experiment_id=experiment_id, experiment_uuid=experiment_uuid)

    if not experiment or not experiment.is_running:
        return False

    return True
