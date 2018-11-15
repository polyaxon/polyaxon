# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_cli.cli.getters.project import get_project_or_local
from polyaxon_cli.managers.experiment_group import GroupManager


def get_group_or_local(group):
    return group or GroupManager.get_config_or_raise().id


def get_project_group_or_local(project=None, group=None):
    user, project_name = get_project_or_local(project)
    group = get_group_or_local(group)
    return user, project_name, group
