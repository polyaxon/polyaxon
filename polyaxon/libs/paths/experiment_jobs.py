import os

from django.conf import settings

from libs.paths.utils import check_archive_path, create_path, delete_path


def get_experiment_job_logs_path(experiment_job_name, temp):
    values = experiment_job_name.split('.')
    values = values[:-2] + ['.'.join(values[-2:])]
    if len(values) == 4:
        values.insert(2, 'experiments')
    else:
        values.insert(2, 'groups')

    if temp:
        return os.path.join(settings.LOGS_MOUNT_PATH, '/'.join(values))
    return os.path.join(settings.LOGS_MOUNT_PATH, '/'.join(values))


def delete_experiment_logs(experiment_job_name):
    path = get_experiment_job_logs_path(experiment_job_name, temp=False)
    delete_path(path)


def create_experiment_job_path(experiment_job_name, path):
    values = experiment_job_name.split('.')
    values = values[:-2] + ['.'.join(values[-2:])]
    if len(values) == 4:
        values.insert(2, 'experiments')
    else:
        values.insert(2, 'groups')

    for value in values[:-2]:
        path = os.path.join(path, value)
        if not os.path.isdir(path):
            create_path(path)

    return path


def create_experiment_job_logs_path(experiment_job_name, temp):
    if temp:
        check_archive_path(settings.LOGS_ARCHIVE_ROOT)
        return create_experiment_job_path(experiment_job_name, settings.LOGS_ARCHIVE_ROOT)
    return create_experiment_job_path(experiment_job_name, settings.LOGS_MOUNT_PATH)
