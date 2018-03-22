import logging

from events import publisher
from experiments.paths import copy_experiment_outputs
from spawners.utils.constants import ExperimentLifeCycle

logger = logging.getLogger('polyaxon.tasks.experiments')


def handle_restarted_experiment(experiment):
    """If experiment is a restart, we should resume from last check point"""
    try:
        publisher.publish_log(
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
        publisher.publish_log(
            log_line='Could not copy the outputs of experiment `{}` into experiment `{}`'.format(
                experiment.original_experiment.unique_name, experiment.unique_name
            ),
            status=ExperimentLifeCycle.BUILDING,
            experiment_uuid=experiment.uuid.hex,
            experiment_name=experiment.unique_name,
            job_uuid='all',
        )
        logger.warning(
            'Could not copy the outputs of experiment `{}` into experiment `{}`'.format(
                experiment.original_experiment.unique_name, experiment.unique_name
            ))
