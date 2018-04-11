from django.apps import AppConfig


class PluginsConfig(AppConfig):
    name = 'plugins'
    verbose_name = 'Plugins'

    def ready(self):
        from plugins.signals import (  # noqa
            new_tensorboard_job,
            new_notebook_job,
            new_tensorboard_job_status,
            new_notebook_job_status,
            project_stop_plugins
        )
