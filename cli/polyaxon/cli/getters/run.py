# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon.cli.getters.project import get_project_or_local
from polyaxon.managers.run import RunManager


def get_run_or_local(run_uuid=None):
    return run_uuid or RunManager.get_config_or_raise().uuid


def get_project_run_or_local(project=None, run_uuid=None):
    user, project_name = get_project_or_local(project)
    run_uuid = get_run_or_local(run_uuid)
    return user, project_name, run_uuid
