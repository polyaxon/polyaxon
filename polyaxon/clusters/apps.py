from django.apps import AppConfig


class ClustersConfig(AppConfig):
    name = 'clusters'
    verbose_name = 'Clusters'

    def ready(self):
        from clusters.signals import cluster_created  # noqa
