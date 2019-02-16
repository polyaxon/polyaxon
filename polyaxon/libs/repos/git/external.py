import logging

from hestia.urls_utils import validate_url

import conf

from libs.repos.git.exceptions import GitCloneException

_logger = logging.getLogger('polyaxon.repos.git')


def get_repo_name(git_url: str) -> str:
    git_name = git_url.split('/')[-1]
    return git_name.split('.git')[0]


def set_git_repo(repo: 'ExternalRepo') -> str:
    from libs.repos.git import clone_git_repo, ensure_repo_paths

    # Ensure paths
    ensure_repo_paths(repo=repo)

    # Create a new repo
    try:
        clone_git_repo(repo_path=repo.path, git_url=repo.git_clone_url)
    except Exception:
        raise GitCloneException('Could not clone git repo, make sure you have access to this repo.')
    return repo.path


def get_private_clone_url(git_url: str) -> str:
    # We make sure that the project has the credentials to use for the private repo
    access_token = conf.get('REPOS_ACCESS_TOKEN')
    if not access_token or not validate_url(git_url):
        raise GitCloneException

    # Add user:pass to the git url
    url = git_url.split('https://')[1]
    return 'https://{}:{}@{}'.format(access_token.user, access_token.password, url)
