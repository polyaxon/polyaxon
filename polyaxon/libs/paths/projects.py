import os

from hestia.paths import delete_path

import conf


def get_project_subpath(project_name: str) -> str:
    return project_name.replace('.', '/')


def get_project_repos_path(project_name: str) -> str:
    return os.path.join(conf.get('REPOS_MOUNT_PATH'), get_project_subpath(project_name))


def delete_project_repos(project_name: str) -> None:
    path = get_project_repos_path(project_name)
    delete_path(path)
