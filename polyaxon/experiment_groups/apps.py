from django.apps import AppConfig


class ExperimentGroupsConfig(AppConfig):
    name = 'experiment_groups'
    verbose_name = 'ExperimentGroups'

    def ready(self):
        from experiment_groups.signals import (  # noqa
            new_experiment_group,
            experiment_group_pre_deleted,
            experiment_group_post_deleted,
            new_experiment_group_iteration
        )
