from django.apps import AppConfig


class RunnerConfig(AppConfig):
    name = 'runner'
    verbose_name = 'Runner'

    def ready(self):
        from runner.signals.experiments import (  # noqa
            start_new_experiment,
            stop_running_experiment,
            handle_new_experiment_status
        )
        from runner.signals.experiment_groups import (  # noqa
            experiment_group_create_experiments,
            experiment_group_stop_experiments
        )
