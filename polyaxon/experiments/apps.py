from django.apps import AppConfig


class ExperimentsConfig(AppConfig):
    name = 'experiments'
    verbose_name = "Experiments"

    def ready(self):
        from experiments.signals import (
            new_experiment,
            experiment_deleted,
            new_experiment_job,
            new_experiment_job_status,
            new_experiment_metric,
        )
