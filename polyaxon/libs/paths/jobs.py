import os

from django.conf import settings

from libs.paths.utils import delete_path, create_path


def get_job_data_path(job_name):
    return os.path.join(settings.DATA_ROOT, job_name.replace('.', '/'))


def get_job_outputs_path(job_name):
    return os.path.join(settings.OUTPUTS_ROOT, job_name.replace('.', '/'))


def get_job_logs_path(job_name):
    return os.path.join(settings.LOGS_ROOT, job_name.replace('.', '/'))


def delete_job_outputs(job_name):
    path = get_job_outputs_path(job_name)
    delete_path(path)


def delete_job_logs(job_name):
    path = get_job_logs_path(job_name)
    delete_path(path)


def create_job_path(job_name, path):
    values = job_name.split('.')

    for value in values[:-1]:
        path = os.path.join(path, value)
        if not os.path.isdir(path):
            create_path(path)

    return path


def create_job_logs_path(job_name):
    return create_job_path(job_name, settings.LOGS_ROOT)


def create_job_outputs_path(job_name):
    values = job_name.split('.')
    path = create_job_path(job_name, settings.OUTPUTS_ROOT)
    path = os.path.join(path, values[-1])
    if not os.path.isdir(path):
        create_path(path)
    return path
