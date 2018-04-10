from django.apps import AppConfig


class RunnerConfig(AppConfig):
    name = 'runner'
    verbose_name = 'Runner'

    def ready(self):
        from runner.signals.experiment_groups import experiment_group_stop_experiments
