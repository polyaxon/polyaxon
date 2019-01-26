import logging
import os

from libs.paths.utils import create_path

_logger = logging.getLogger('polyaxon.repos.git')


def set_git_repo(repo):
    from libs.repos.git import get_git_repo

    # Check that the user has a dir
    if not os.path.isdir(repo.user_path):
        create_path(repo.user_path)

    # Check that the project has a dir
    if not os.path.isdir(repo.project_path):
        create_path(repo.project_path)

    # Create a new repo
    get_git_repo(repo_path=repo.path, init=True)
