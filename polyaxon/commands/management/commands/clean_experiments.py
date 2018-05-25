from django.core.management import BaseCommand
from django.db import ProgrammingError

from constants.experiments import ExperimentLifeCycle
from db.models.experiments import Experiment
from scheduler import experiment_scheduler


class Command(BaseCommand):
    @staticmethod
    def _clean():
        for experiment in Experiment.objects.filter(
                experiment_status__status__in=ExperimentLifeCycle.RUNNING_STATUS):
            experiment_scheduler.stop_experiment(experiment, update_status=True)

    def handle(self, *args, **options):
        try:
            self._clean()
        except ProgrammingError:
            pass
