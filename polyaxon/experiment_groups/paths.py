import os

from django.conf import settings

from libs.paths import delete_path


def get_experiment_group_outputs_path(experiment_group_name):
    return os.path.join(settings.OUTPUTS_ROOT, experiment_group_name.replace('.', '/'))


def get_experiment_group_logs_path(experiment_group_name):
    return os.path.join(settings.LOGS_ROOT, experiment_group_name.replace('.', '/'))


def delete_experiment_group_outputs(experiment_group_name):
    path = get_experiment_group_outputs_path(experiment_group_name)
    delete_path(path)


def delete_experiment_group_logs(experiment_group_name):
    path = get_experiment_group_logs_path(experiment_group_name)
    delete_path(path)
