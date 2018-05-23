import logging

from db.models.experiment_groups import ExperimentGroup

logger = logging.getLogger('polyaxon.experiment_groups.utils')


def get_valid_experiment_group(experiment_group_id):
    try:
        return ExperimentGroup.objects.get(id=experiment_group_id)
    except ExperimentGroup.DoesNotExist:
        logger.info('ExperimentGroup `%s` was not found.', experiment_group_id)
        return None


def get_running_experiment_group(experiment_group_id):
    experiment_group = get_valid_experiment_group(experiment_group_id=experiment_group_id)

    if not experiment_group.is_running:
        logger.info('ExperimentGroup `%s` is not running.', experiment_group_id)
        return None

    return experiment_group
