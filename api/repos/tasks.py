# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from api.settings import CeleryTasks
from api.celery_api import app as celery_app

logger = logging.getLogger('polyaxon.tasks.repos')


@celery_app.task(name=CeleryTasks.REPOS_HANDLE_FILE_UPLOAD)
def handle_new_files(user_id, repo_id, tar_file_name):
    # untar the file
    # move all files to the corect repo
    # commit changes
    # add new revision to repo
    pass
