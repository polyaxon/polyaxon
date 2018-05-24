from django.apps import AppConfig


class SuggesterConfig(AppConfig):
    name = 'suggester'
    verbose_name = 'Suggester'

    from suggester.signals import new_experiment_group_iteration  # noqa
