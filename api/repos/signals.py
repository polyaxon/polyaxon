# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import shutil

import os

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from repos import git
from repos.models import ExternalRepo, Repo


@receiver(post_save, sender=Repo, dispatch_uid="repo_saved")
def new_repo(sender, **kwargs):
    if kwargs.get('raw'):
        # Ignore signal handling for fixture loading
        return

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


@receiver(post_delete, sender=ExternalRepo, dispatch_uid="repo_deleted")
def repo_deleted(sender, **kwargs):
    if kwargs.get('raw'):
        # Ignore signal handling for fixture loading
        return

    instance = kwargs['instance']

    # Clean repo
    shutil.rmtree(instance.path)


@receiver(post_save, sender=ExternalRepo, dispatch_uid="external_repo_saved")
def new_external_repo(sender, **kwargs):
    if kwargs.get('raw'):
        # Ignore signal handling for fixture loading
        return

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


@receiver(post_delete, sender=Repo, dispatch_uid="external_repo_deleted")
def external_repo_deleted(sender, **kwargs):
    if kwargs.get('raw'):
        # Ignore signal handling for fixture loading
        return

    instance = kwargs['instance']

    # Clean repo
    shutil.rmtree(instance.path)
