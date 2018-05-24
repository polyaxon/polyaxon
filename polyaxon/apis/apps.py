from django.apps import AppConfig


class APIsConfig(AppConfig):
    name = 'apis'
    verbose_name = 'APIs'

    def ready(self):
        from signals.experiments import *  # noqa
        from signals.experiment_groups import *  # noqa
        from signals.projects import *  # noqa
        from signals.project_plugin_jobs import *  # noqa
        from signals.nodes import *  # noqa
