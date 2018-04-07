# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon_cli.managers.base import BaseConfigManager
from polyaxon_cli.utils.formatting import Printer
from polyaxon_schemas.project import ProjectConfig


class ProjectManager(BaseConfigManager):
    """Manages project configuration .polyaxonproject file."""

    IS_GLOBAL = False
    IS_POLYAXON_DIR = True
    CONFIG_FILE_NAME = '.polyaxonproject'
    CONFIG = ProjectConfig

    @classmethod
    def get_config_or_raise(cls):
        project = cls.get_config()
        if not project:
            Printer.print_error('Please initialize your project before uploading any code.'
                                '`polyaxon init PROJECT_NAME [--run|--model]`')
            sys.exit(1)

        return project
