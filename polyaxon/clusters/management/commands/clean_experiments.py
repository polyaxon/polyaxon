# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.core.management import BaseCommand
from django.db import ProgrammingError

from experiments.models import Experiment
from schedulers import experiment_scheduler
from spawners.utils.constants import ExperimentLifeCycle


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
