import logging
import os

import conf

from libs.paths.utils import create_path

_logger = logging.getLogger('polyaxon.repos.git')


def get_repo_name(git_url: str) -> str:
    git_name = git_url.split('/')[-1]
    return git_name.split('.git')[0]


def set_git_repo(git_url: str):
    from libs.repos.git import get_git_repo

    mount_path = conf.get('REPOS_MOUNT_PATH')
    repo_name = get_repo_name(git_url=git_url)
    repo_owner = repo_name.split('/')[0]

    # Check that the owner has a dir
    owner_path = '{}/{}'.format(mount_path, repo_owner)
    if not os.path.isdir(owner_path):
        create_path(owner_path)

    # Check that the project has a dir
    repo_path = '{}/{}'.format(mount_path, repo_name)
    if not os.path.isdir(repo_path):
        create_path(repo_path)

    # Create a new repo
    get_git_repo(repo_path=repo_path, init=True)
