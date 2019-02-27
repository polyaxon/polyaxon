import logging
import os
import shlex

from subprocess import PIPE

from typing import Tuple, Any, List, Optional, Union

from git import InvalidGitRepositoryError
from git import Repo as GitRepo
from hestia.paths import create_path, delete_path
from psutil import Popen

from libs.repos.git.exceptions import GitCloneException
from libs.repos.git import internal, external  # noqa

_logger = logging.getLogger('polyaxon.repos.git')


def ensure_repo_paths(repo: Union['Repo', 'ExternalRepo']):
    # Check that the user has a dir
    if not os.path.isdir(repo.user_path):
        create_path(repo.user_path)

    # Check that the project has a dir
    if not os.path.isdir(repo.project_path):
        create_path(repo.project_path)


def get_git_repo(repo_path: str, init: bool = False) -> Any:
    if os.path.isdir(repo_path):
        try:
            return GitRepo(repo_path)
        except InvalidGitRepositoryError:
            if init:
                return GitRepo.init(repo_path)
    elif init:
        try:
            create_path(repo_path)
            return get_git_repo(repo_path, init=init)
        except FileNotFoundError:
            pass

    raise ValueError('Could not create a repo on this path {}'.format(repo_path))


def clone_git_repo(repo_path: str, git_url: str) -> str:
    return GitRepo.clone_from(url=git_url, to_path=repo_path)


def get_status(repo_path: str) -> str:
    return run_command(cmd='git status -s', data=None, location=repo_path, chw=True)


def commit(repo_path: str, user_email: str, user_name: str, message: str = 'updated') -> None:
    run_command(cmd='git add -A', data=None, location=repo_path, chw=True)
    run_command(cmd='git -c user.email=<{}> -c user.name={} commit -m "{}"'.format(
        user_email, user_name, message),
        data=None, location=repo_path, chw=True)


def get_commit(repo_path: str, commit: Any) -> Any:  # pylint:disable=redefined-outer-name
    repo = get_git_repo(repo_path)
    commit = repo.commit(commit)
    return commit


def get_last_commit(repo_path: str) -> Tuple:
    commit_hash = run_command(cmd='git --no-pager log --pretty=oneline -1', data=None,
                              location=repo_path, chw=True).split(' ')[0]

    if commit_hash:
        return commit_hash, get_commit(repo_path, commit_hash)
    raise ValueError('Commit was not found.')


def undo(repo_path: str) -> None:
    run_command(cmd='git reset --hard', data=None, location=repo_path, chw=True)
    run_command(cmd='git clean -fd', data=None, location=repo_path, chw=True)


def get_committed_files(repo_path: str,
                        commit: Any) -> List[str]:  # pylint:disable=redefined-outer-name
    files_committed = run_command(
        cmd='git diff-tree --no-commit-id --name-only -r {}'.format(commit),
        data=None, location=repo_path, chw=True).split('\n')
    return [f for f in files_committed if f]


def fetch(git_url: str,
          repo_path: str,
          overwrite: bool = False,
          branch='master',
          reset_remote=False) -> Optional[Any]:
    if reset_remote:
        set_remote(repo_path=repo_path, git_url=git_url)

    branch = branch or 'master'
    if os.path.isdir(repo_path):
        _logger.info('Current checkout path has content.')
        if overwrite:
            _logger.info('Overwriting current checkout path.')
            delete_path(repo_path)
        else:
            run_command(cmd='git fetch origin {}'.format(branch),
                        data=None,
                        location=repo_path,
                        chw=True)
            checkout_commit(repo_path=repo_path, commit=branch)
            run_command(cmd='git fetch origin {}'.format(branch),
                        data=None,
                        location=repo_path,
                        chw=True)
            run_command(cmd='git reset --hard FETCH_HEAD', data=None, location=repo_path, chw=True)
            run_command(cmd='git clean -df', data=None, location=repo_path, chw=True)
            return None
    return clone_git_repo(repo_path=repo_path, git_url=git_url)


def checkout_commit(repo_path: str,
                    commit: Any = None) -> None:  # pylint:disable=redefined-outer-name
    """Checkout to a specific commit.

    If commit is None then checkout to master.
    """
    commit = commit or 'master'
    run_command(cmd='git checkout {}'.format(commit), data=None, location=repo_path, chw=True)


def run_command(cmd: str, data: Optional[str], location: str, chw: bool) -> str:
    cwd = os.getcwd()

    if location is not None and chw is True:
        cwd = location
    elif location is not None and chw is False:
        cmd = '{0} {1}'.format(cmd, location)

    r = Popen(shlex.split(cmd), stdout=PIPE, stdin=PIPE, stderr=PIPE, cwd=cwd)

    if data is None:
        output = r.communicate()[0].decode('utf-8')
    else:
        output = r.communicate(input=data)[0]

    return output


def get_remote(repo_path: str) -> str:
    current_remote = run_command(cmd='git config --get remote.origin.url {}'.format(repo_path),
                                 data=None,
                                 location=repo_path,
                                 chw=True)
    return current_remote.strip('\n')


def set_remote(repo_path: str, git_url: str) -> None:
    run_command(cmd='git remote set-url origin {}'.format(git_url),
                data=None,
                location=repo_path,
                chw=True)

