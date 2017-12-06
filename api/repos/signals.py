# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import shutil

from repos import git


def new_repo(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    # Check if the experiment is newly created and that we can start it independently
    if not created:
        return

    # Create a new repo
    git.get_git_repo(repo_path=instance.path, init=True)


def repo_deleted(sender, **kwargs):
    instance = kwargs['instance']

    # Clean repo
    shutil.rmtree(instance.path)
