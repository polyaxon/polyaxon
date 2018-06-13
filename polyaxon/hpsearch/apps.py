from django.apps import AppConfig


class HPSearchConfig(AppConfig):
    name = 'hpsearch'
    verbose_name = 'HP Search'

    def ready(self):
        from hpsearch.signals import new_experiment_group_iteration  # noqa
        import signals.experiments  # noqa
        import signals.experiment_groups  # noqa
