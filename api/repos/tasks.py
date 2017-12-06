# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import tarfile

import os
import shutil

from django.conf import settings
from django.contrib.auth import get_user_model

from api.settings import CeleryTasks
from api.celery_api import app as celery_app
from repos import git
from repos.models import Repo, RepoRevision

logger = logging.getLogger('polyaxon.tasks.repos')


@celery_app.task(name=CeleryTasks.REPOS_HANDLE_FILE_UPLOAD)
def handle_new_files(user_id, repo_id, tar_file_name):
    if not tarfile.is_tarfile(tar_file_name):
        raise ValueError('Received wrong file format.')

    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.warning('User with id `{}` does not exists anymore.'.format(user_id))
        return

    try:
        repo = Repo.objects.get(id=repo_id)
    except User.DoesNotExist:
        logger.warning('Repo with id `{}` does not exists anymore.'.format(repo_id))
        return

    # Destination files
    repo_name = repo.project
    repo_path = os.path.join(settings.REPOS_ROOT, user.username, repo_name)
    new_repo_path = os.path.join(repo_path, '{}_new.tar.gz'.format(repo_name))

    # clean the current path from all files
    for member in os.listdir(repo_path):
        if member == '.git':
            continue
        if os.path.isfile(member):
            os.remove(member)
        else:
            shutil.rmtree(member)

    # Move the tar inside the repo path
    shutil.move(tar_file_name, new_repo_path)

    # Untar the file
    with tarfile.open(new_repo_path) as tar:
        files = [f.name for f in tar]
        tar.extractall()

    # Delete the current tar
    os.remove(new_repo_path)

    # Get the git repo
    if not git.get_status(repo_path):
        return

    # commit changes
    git.commit(repo_path, user.email, user.name)
    # add new revision to repo
    hash, commit = git.get_last_commit(repo_path=repo_path)
    message = commit.summary
    RepoRevision(repo=repo, user=user, commit=hash, message=message).save()
