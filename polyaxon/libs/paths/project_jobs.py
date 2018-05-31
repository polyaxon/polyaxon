import os

from django.conf import settings

from libs.paths.utils import delete_path


def get_project_job_outputs_path(job_name):
    return os.path.join(settings.OUTPUTS_ROOT, job_name.replace('.', '/'))


def get_project_job_logs_path(job_name):
    return os.path.join(settings.LOGS_ROOT, job_name.replace('.', '/'))


def delete_project_job_outputs(job_name):
    path = get_project_job_outputs_path(job_name)
    delete_path(path)


def delete_project_job_logs(job_name):
    path = get_project_job_logs_path(job_name)
    delete_path(path)
