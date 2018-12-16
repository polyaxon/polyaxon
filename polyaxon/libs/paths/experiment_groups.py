import os

import stores

from libs.paths.utils import delete_path


def get_experiment_group_outputs_path(persistence_outputs, experiment_group_name):
    persistence_outputs = stores.get_outputs_paths(persistence_outputs)
    values = experiment_group_name.split('.')
    values.insert(2, 'groups')
    return os.path.join(persistence_outputs, '/'.join(values))


def get_experiment_group_logs_path(experiment_group_name):
    values = experiment_group_name.split('.')
    values.insert(2, 'groups')
    persistence_logs = stores.get_logs_paths()
    return os.path.join(persistence_logs, '/'.join(values))


def delete_experiment_group_outputs(persistence_outputs, experiment_group_name):
    path = get_experiment_group_outputs_path(persistence_outputs, experiment_group_name)
    delete_path(path)  # TODO: should use polystores


def delete_experiment_group_logs(experiment_group_name):
    path = get_experiment_group_logs_path(experiment_group_name)
    delete_path(path)  # TODO: should use polystores
