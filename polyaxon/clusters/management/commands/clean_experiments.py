from django.core.management import BaseCommand

from experiments.models import Experiment
from schedulers import experiment_scheduler
from spawners.utils.constants import ExperimentLifeCycle


class Command(BaseCommand):
    def handle(self, *args, **options):
        for experiment in Experiment.objects.filter(
                experiment_status__status__in=ExperimentLifeCycle.RUNNING_STATUS):
            experiment_scheduler.stop_experiment(experiment, update_status=True)
