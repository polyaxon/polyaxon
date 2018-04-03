from django.apps import AppConfig


class ExperimentGroupsConfig(AppConfig):
    name = 'experiment_groups'
    verbose_name = 'ExperimentGroups'

    def ready(self):
        from experiment_groups.signals import (
            new_experiment_group,
            experiment_group_deleted,
        )
