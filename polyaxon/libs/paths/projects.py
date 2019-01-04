import os

from django.conf import settings

from libs.paths.utils import delete_path


def get_project_subpath(project_name):
    return project_name.replace('.', '/')


def get_project_repos_path(project_name):
    return os.path.join(settings.REPOS_MOUNT_PATH, get_project_subpath(project_name))


def delete_project_repos(project_name):
    path = get_project_repos_path(project_name)
    delete_path(path)
