import logging

from db.models.experiment_groups import ExperimentGroup

_logger = logging.getLogger('polyaxon.db')


def get_valid_experiment_group(experiment_group_id):
    try:
        return ExperimentGroup.objects.get(id=experiment_group_id)
    except ExperimentGroup.DoesNotExist:
        _logger.info('ExperimentGroup `%s` was not found.', experiment_group_id)
        return None


def get_running_experiment_group(experiment_group_id):
    experiment_group = get_valid_experiment_group(experiment_group_id=experiment_group_id)

    if not experiment_group.is_running:
        _logger.info('ExperimentGroup `%s` is not running.', experiment_group_id)
        return None

    return experiment_group
