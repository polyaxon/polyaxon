from django.apps import AppConfig


class NodesConfig(AppConfig):
    name = 'nodes'
    verbose_name = 'Nodes'

    def ready(self):
        from nodes.signals import node_gpu_created  # noqa
