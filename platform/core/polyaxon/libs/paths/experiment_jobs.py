import os

from hestia.paths import create_path


def get_experiment_job_subpath(experiment_job_name: str) -> str:
    values = experiment_job_name.split('.')
    values = values[:-2] + ['.'.join(values[-2:])]
    if len(values) == 4:
        values.insert(2, 'experiments')
    else:
        values.insert(2, 'groups')

    return '/'.join(values)


def create_experiment_job_path(experiment_job_name: str, path: str) -> str:
    values = experiment_job_name.split('.')
    values = values[:-2] + ['.'.join(values[-2:])]
    if len(values) == 4:
        values.insert(2, 'experiments')
    else:
        values.insert(2, 'groups')

    for value in values[:-1]:
        path = os.path.join(path, value)
        if not os.path.isdir(path):
            create_path(path)

    return path
