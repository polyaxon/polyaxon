# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from polyaxon_client.tracking.utils.cmd import run_command


def is_git_initialized(path='.'):
    return bool(run_command(cmd='git rev-parse --is-inside-work-tree',
                            data=None,
                            location=path,
                            chw=True).split('\n')[0])


def get_commit(path='.'):
    return run_command(cmd='git --no-pager log --pretty=oneline -1',
                       data=None,
                       location=path,
                       chw=True).split(' ')[0]


def get_head(path='.'):
    return run_command(cmd='git rev-parse HEAD',
                       data=None,
                       location=path,
                       chw=True).split('\n')[0]


def get_remote(path='.'):
    return run_command(cmd='git config --get remote.origin.url',
                       data=None,
                       location=path,
                       chw=True).split('\n')[0]


def get_repo_name(path='.'):
    repo = run_command(cmd='git rev-parse --show-toplevel',
                       data=None,
                       location=path,
                       chw=True).split('\n')[0]

    return os.path.basename(repo)


def get_branch_name(path='.'):
    return run_command(cmd='git rev-parse --abbrev-ref HEAD',
                       data=None,
                       location=path,
                       chw=True).split('\n')[0]


def is_dirty(path='.'):
    return bool(run_command(cmd='git diff --stat',
                            data=None,
                            location=path,
                            chw=True))


def get_code_reference(path='.'):
    if not is_git_initialized(path):
        return None

    return {
        'commit': get_commit(path),
        'head': get_head(path),
        'branch': get_branch_name(path),
        'git_url': get_remote(path),
        'is_dirty': is_dirty(path),
    }
