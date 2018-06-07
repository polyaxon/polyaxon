import os

from django.conf import settings

from libs.paths.utils import delete_path


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
