import logging

from experiment_groups.models import ExperimentGroup

logger = logging.getLogger('polyaxon.experiment_groups.utils')


def get_valid_experiment_group(experiment_group_id):
    try:
        return ExperimentGroup.objects.get(id=experiment_group_id)
    except ExperimentGroup.DoesNotExist:
        logger.info('ExperimentGroup `{}` was not found.'.format(experiment_group_id))
        return None
