# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon_cli.managers.base import BaseConfigManager
from polyaxon_cli.schemas import ProjectConfig
from polyaxon_cli.utils import constants
from polyaxon_cli.utils.formatting import Printer


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
                                ' {}'.format(constants.INIT_COMMAND))
            sys.exit(1)

        return project
