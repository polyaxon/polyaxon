import os
import shutil

from django.conf import settings

import stores

from db.models.cloning_strategies import CloningStrategy
from libs.paths.utils import check_archive_path, create_path, delete_path


def get_experiment_outputs_path(persistence_outputs,
                                experiment_name,
                                original_name=None,
                                cloning_strategy=None):
    persistence_outputs = stores.get_outputs_paths(persistence_outputs)
    values = experiment_name.split('.')
    if original_name is not None and cloning_strategy == CloningStrategy.RESUME:
        values = original_name.split('.')
    if len(values) == 3:
        values.insert(2, 'experiments')
    else:
        values.insert(2, 'groups')
    return os.path.join(persistence_outputs, '/'.join(values))


def get_experiment_logs_path(experiment_name, temp):
    values = experiment_name.split('.')
    if len(values) == 3:
        values.insert(2, 'experiments')
    else:
        values.insert(2, 'groups')

    if temp:
        return os.path.join(settings.LOGS_ARCHIVE_ROOT, '/'.join(values))
    persistence_logs = stores.get_logs_paths()
    return os.path.join(persistence_logs, '/'.join(values))


def delete_experiment_logs(experiment_name):
    path = get_experiment_logs_path(experiment_name, temp=False)
    delete_path(path)


def delete_experiment_outputs(persistence_outputs, experiment_name):
    path = get_experiment_outputs_path(persistence_outputs, experiment_name)
    delete_path(path)  # TODO: should use polystores


def create_experiment_path(experiment_name, path):
    values = experiment_name.split('.')
    if len(values) == 3:
        values.insert(2, 'experiments')
    else:
        values.insert(2, 'groups')

    for value in values[:-1]:
        path = os.path.join(path, value)
        if not os.path.isdir(path):
            create_path(path)

    return path


def create_experiment_logs_path(experiment_name, temp):
    if temp:
        check_archive_path(settings.LOGS_ARCHIVE_ROOT)
        return create_experiment_path(experiment_name, settings.LOGS_ARCHIVE_ROOT)

    persistence_logs = stores.get_logs_paths()
    return create_experiment_path(experiment_name, persistence_logs)


def create_experiment_outputs_path(persistence_outputs, experiment_name):
    persistence_outputs = stores.get_outputs_paths(persistence_outputs)
    values = experiment_name.split('.')
    path = create_experiment_path(experiment_name, persistence_outputs)
    path = os.path.join(path, values[-1])
    if not os.path.isdir(path):
        create_path(path)
    return path


def copy_experiment_outputs(persistence_outputs_from,
                            persistence_outputs_to,
                            experiment_name_from,
                            experiment_name_to):
    path_from = get_experiment_outputs_path(persistence_outputs_from, experiment_name_from)
    path_to = get_experiment_outputs_path(persistence_outputs_to, experiment_name_to)
    shutil.copytree(path_from, path_to)
