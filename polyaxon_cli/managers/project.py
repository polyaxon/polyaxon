# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.project import ProjectConfig

from polyaxon_cli.managers.base import BaseConfigManager


class ProjectManager(BaseConfigManager):
    """Manages access token configuration .plxprojectconfig file."""

    IS_GLOBAL = False
    CONFIG_FILE_NAME = '.polyaxonproject'
    CONFIG = ProjectConfig
