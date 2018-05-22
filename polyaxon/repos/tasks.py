import logging
import os
import shutil
import tarfile

from django.contrib.auth import get_user_model

import auditor

from event_manager.events.repo import REPO_NEW_COMMIT
from libs.paths import delete_path
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import CeleryTasks
from repos import git
from models.repos import Repo

logger = logging.getLogger('polyaxon.tasks.repos')


@celery_app.task(name=CeleryTasks.REPOS_HANDLE_FILE_UPLOAD, ignore_result=True)
def handle_new_files(user_id, repo_id, tar_file_name):
    if not tarfile.is_tarfile(tar_file_name):
        raise ValueError('Received wrong file format.')

    User = get_user_model()  # noqa
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.warning('User with id `%s` does not exist anymore.', user_id)
        return

    try:
        repo = Repo.objects.get(id=repo_id)
        # Checkout to master
        git.checkout_commit(repo.path)
    except User.DoesNotExist:
        logger.warning('Repo with id `%s` does not exist anymore.', repo_id)
        return

    # Destination files
    new_repo_path = repo.get_tmp_tar_path()

    # clean the current path from all files
    path_files = os.listdir(repo.path)
    for member in path_files:
        if member == '.git':
            continue
        member = os.path.join(repo.path, member)
        if os.path.isfile(member):
            os.remove(member)
        else:
            delete_path(member)

    # Move the tar inside the repo path
    shutil.move(tar_file_name, new_repo_path)

    # Untar the file
    with tarfile.open(new_repo_path) as tar:
        tar.extractall(repo.path)

    # Delete the current tar
    os.remove(new_repo_path)

    # Get the git repo
    if not git.get_status(repo.path):
        return

    # commit changes
    git.commit(repo.path, user.email, user.username)
    auditor.record(event_type=REPO_NEW_COMMIT, instance=repo, actor_id=user.id)
