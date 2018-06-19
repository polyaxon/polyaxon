# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon_cli.managers.base import BaseConfigManager
from polyaxon_cli.utils.formatting import Printer
from polyaxon_schemas.project import ExperimentGroupConfig


class GroupManager(BaseConfigManager):
    """Manages experiment configuration .polyaxongroup file."""

    IS_GLOBAL = False
    IS_POLYAXON_DIR = True
    CONFIG_FILE_NAME = '.polyaxongroup'
    CONFIG = ExperimentGroupConfig

    @classmethod
    def get_config_or_raise(cls):
        experiment_group = cls.get_config()
        if not experiment_group:
            Printer.print_error('No group id was provided.')
            sys.exit(1)

        return experiment_group
