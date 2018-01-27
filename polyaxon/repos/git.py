# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import os
import shlex
import shutil
from subprocess import PIPE

from django.conf import settings
from git import Repo as GitRepo, InvalidGitRepositoryError
from psutil import Popen

logger = logging.getLogger('polyaxon.repos.git')


def get_repos(user):
    user_repos_root = os.path.join(settings.REPOS_ROOT, user)
    repos = [get_git_repo(os.path.join(user, dir)) for dir in os.listdir(user_repos_root)]
    return [repo for repo in repos if not (repo is None)]


def get_git_repo(repo_path, init=False):
    if os.path.isdir(repo_path):
        try:
            return GitRepo(repo_path)
        except InvalidGitRepositoryError:
            if init:
                return GitRepo.init(repo_path)
    elif init:
        try:
            os.mkdir(repo_path)
            return get_git_repo(repo_path, init=init)
        except FileNotFoundError:
            pass

    raise ValueError('Could not create a repo on this path {}'.format(repo_path))


def clone_git_repo(repo_path, git_url):
    return GitRepo.clone_from(url=git_url, to_path=repo_path)


def get_status(repo_path):
    return run_command(cmd='git status -s', data=None, location=repo_path, chw=True)


def commit(repo_path, user_email, user_name, message='updated'):
    run_command(cmd='git add -A', data=None, location=repo_path, chw=True)
    run_command(cmd='git -c user.email=<{}> -c user.name={} commit -m "{}"'.format(
        user_email, user_name, message),
        data=None, location=repo_path, chw=True)


def get_last_commit(repo_path):
    commit_hash = run_command(cmd='git --no-pager log --pretty=oneline -1', data=None,
                              location=repo_path, chw=True).split(' ')[0]

    return (commit_hash, get_commit(repo_path, commit_hash)) if commit_hash else None


def get_commit(repo_path, commit):
    repo = get_git_repo(repo_path)
    commit = repo.commit(commit)
    return commit


def get_committed_files(repo_path, commit):
    files_committed = run_command(
        cmd='git diff-tree --no-commit-id --name-only -r {}'.format(commit),
        data=None, location=repo_path, chw=True).split('\n')
    return [f for f in files_committed if f]


def fetch(git_url, repo_path, overwrite=False):
    if os.path.isdir(repo_path):
        logger.info('Current checkout path has content.')
        if overwrite:
            logger.info('Overwriting current checkout path.')
            shutil.rmtree(repo_path)
        else:
            run_command(cmd='git fetch origin master', data=None, location=repo_path, chw=True)
            run_command(cmd='git reset --hard FETCH_HEAD', data=None, location=repo_path, chw=True)
            run_command(cmd='git clean -df', data=None, location=repo_path, chw=True)
            return
    return clone_git_repo(repo_path=repo_path, git_url=git_url)


def archive_repo(repo, repo_name):
    with open(os.path.join(settings.REPOS_ARCHIVE_ROOT, '{}.tar'.format(repo_name)), 'wb') as fp:
        repo.archive(fp)


def checkout_commit(repo_path, commit=None):
    """Checkout to a specific commit.

    If commit is None then checkout to master.
    """
    commit = commit or '-'
    run_command(cmd='git checkout {}'.format(commit), data=None, location=repo_path, chw=True)


def run_command(cmd, data, location, chw):
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
