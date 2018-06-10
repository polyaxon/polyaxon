from django.core.management import BaseCommand
from django.db import ProgrammingError

from constants.experiments import ExperimentLifeCycle
from db.models.experiments import Experiment
from scheduler import experiment_scheduler


class Command(BaseCommand):
    @staticmethod
    def _clean():
        for experiment in Experiment.objects.filter(
                status__status__in=ExperimentLifeCycle.RUNNING_STATUS):
            group = experiment.experiment_group
            experiment_scheduler.stop_experiment(
                project_name=experiment.project.unique_name,
                project_uuid=experiment.project.uuid.hex,
                experiment_name=experiment.unique_name,
                experiment_uuid=experiment.unique_name,
                experiment_group_name=group.unique_name if group else None,
                experiment_group_uuid=group.uuid.hex if group else None,
                specification=experiment.specification)
            experiment.set_status(ExperimentLifeCycle.STOPPED, message='Cleanup')

    def handle(self, *args, **options):
        try:
            self._clean()
        except ProgrammingError:
            pass
