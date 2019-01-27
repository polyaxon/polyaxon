from constants.experiments import ExperimentLifeCycle
from db.models.experiments import Experiment
from libs.base_clean import BaseCleanCommand
from scheduler import experiment_scheduler


class Command(BaseCleanCommand):
    @staticmethod
    def _clean() -> None:
        for experiment in Experiment.objects.filter(
                status__status__in=ExperimentLifeCycle.RUNNING_STATUS):
            group = experiment.experiment_group
            experiment_scheduler.stop_experiment(
                project_name=experiment.project.unique_name,
                project_uuid=experiment.project.uuid.hex,
                experiment_name=experiment.unique_name,
                experiment_uuid=experiment.uuid.hex,
                experiment_group_name=group.unique_name if group else None,
                experiment_group_uuid=group.uuid.hex if group else None,
                specification=experiment.specification)
            experiment.set_status(ExperimentLifeCycle.STOPPED,
                                  message='Stop triggered by the cleaning hook.')
