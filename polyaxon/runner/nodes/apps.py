from django.apps import AppConfig


class NodesConfig(AppConfig):
    name = 'runner.nodes'
    verbose_name = 'Nodes'

    def ready(self):
        from runner.nodes.signals import node_gpu_created  # noqa
