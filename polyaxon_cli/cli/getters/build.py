# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_cli.cli.getters.project import get_project_or_local
from polyaxon_cli.managers.build_job import BuildJobManager


def get_build_or_local(project=None, build=None):
    user, project_name = get_project_or_local(project)
    build = build or BuildJobManager.get_config_or_raise().id
    return user, project_name, build
