# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import shutil

import os

from repos import git


def new_repo(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    # Check if the experiment is newly created and that we can start it independently
    if not created:
        return

    # Check that the user has a dir
    if not os.path.isdir(instance.user_path):
        os.mkdir(instance.user_path)

    # Check that the project has a dir
    if not os.path.isdir(instance.project_path):
        os.mkdir(instance.project_path)

    # Create a new repo
    git.get_git_repo(repo_path=instance.path, init=True)


def repo_deleted(sender, **kwargs):
    instance = kwargs['instance']

    # Clean repo
    shutil.rmtree(instance.path)


def new_external_repo(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    # Check if the experiment is newly created and that we can start it independently
    if not created:
        return

    # Check that the user has a dir
    if not os.path.isdir(instance.user_path):
        os.mkdir(instance.user_path)

    # Check that the project has a dir
    if not os.path.isdir(instance.project_path):
        os.mkdir(instance.project_path)

    # Create a new repo
    git.clone_git_repo(repo_path=instance.path, git_url=instance.git_url)


def external_repo_deleted(sender, **kwargs):
    instance = kwargs['instance']

    # Clean repo
    shutil.rmtree(instance.path)
