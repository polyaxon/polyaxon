import os

from django.conf import settings

from libs.paths.outputs_paths import get_outputs_paths
from libs.paths.utils import delete_path


def get_project_outputs_path(persistence_outputs, project_name):
    persistence_outputs = get_outputs_paths(persistence_outputs)
    return os.path.join(persistence_outputs, project_name.replace('.', '/'))


def get_project_logs_path(project_name):
    return os.path.join(settings.LOGS_ROOT, project_name.replace('.', '/'))


def get_project_repos_path(project_name):
    return os.path.join(settings.REPOS_ROOT, project_name.replace('.', '/'))


def delete_project_outputs(persistence_outputs, project_name):
    path = get_project_outputs_path(persistence_outputs, project_name)
    delete_path(path)


def delete_project_logs(project_name):
    path = get_project_logs_path(project_name)
    delete_path(path)


def delete_project_repos(project_name):
    path = get_project_repos_path(project_name)
    delete_path(path)
