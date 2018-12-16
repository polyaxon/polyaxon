import os

from django.conf import settings

import stores

from libs.paths.utils import check_archive_path, create_path, delete_path


def get_job_outputs_path(persistence_outputs, job_name):
    persistence_outputs = stores.get_outputs_paths(persistence_outputs)
    return os.path.join(persistence_outputs, job_name.replace('.', '/'))


def get_job_logs_path(job_name, temp):
    if temp:
        return os.path.join(settings.LOGS_ARCHIVE_ROOT, job_name.replace('.', '/'))
    persistence_logs = stores.get_logs_paths()
    return os.path.join(persistence_logs, job_name.replace('.', '/'))


def delete_job_outputs(persistence_outputs, job_name):
    path = get_job_outputs_path(persistence_outputs, job_name)
    delete_path(path)  # TODO: should use polystores


def delete_job_logs(job_name):
    path = get_job_logs_path(job_name, temp=False)
    delete_path(path)  # TODO: should use polystores


def create_job_path(job_name, path):
    values = job_name.split('.')

    for value in values[:-1]:
        path = os.path.join(path, value)
        if not os.path.isdir(path):
            create_path(path)

    return path


def create_job_logs_path(job_name, temp):
    if temp:
        check_archive_path(settings.LOGS_ARCHIVE_ROOT)
        return create_job_path(job_name, settings.LOGS_ARCHIVE_ROOT)
    persistence_logs = stores.get_logs_paths()
    return create_job_path(job_name, persistence_logs)


def create_job_outputs_path(persistence_outputs, job_name):
    persistence_outputs = stores.get_outputs_paths(persistence_outputs)
    values = job_name.split('.')
    path = create_job_path(job_name, persistence_outputs)
    path = os.path.join(path, values[-1])
    if not os.path.isdir(path):
        create_path(path)
    return path
