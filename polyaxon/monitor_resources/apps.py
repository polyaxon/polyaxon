from django.apps import AppConfig


class MonitorResourcesConfig(AppConfig):
    name = 'monitor_resources'
    verbose_name = 'Monitor Resources'

    def ready(self):
        from signals.nodes import node_gpu_created  # noqa
