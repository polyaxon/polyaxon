from django.apps import AppConfig


class ResourcesMonitorConfig(AppConfig):
    name = 'resources_monitor'
    verbose_name = 'Resources Monitor'

    def ready(self):
        from signals.nodes import node_gpu_created  # noqa
