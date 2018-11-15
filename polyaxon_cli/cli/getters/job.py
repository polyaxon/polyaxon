# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_cli.cli.getters.project import get_project_or_local
from polyaxon_cli.managers.job import JobManager


def get_job_or_local(project=None, job=None):
    user, project_name = get_project_or_local(project)
    job = job or JobManager.get_config_or_raise().id
    return user, project_name, job
