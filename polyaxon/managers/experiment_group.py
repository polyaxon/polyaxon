# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon.managers.base import BaseConfigManager
from polyaxon.schemas import GroupConfig
from polyaxon.utils.formatting import Printer


class GroupManager(BaseConfigManager):
    """Manages experiment configuration .polyaxongroup file."""

    IS_GLOBAL = False
    IS_POLYAXON_DIR = True
    CONFIG_FILE_NAME = '.polyaxongroup'
    CONFIG = GroupConfig

    @classmethod
    def get_config_or_raise(cls):
        experiment_group = cls.get_config()
        if not experiment_group:
            Printer.print_error('No group id was provided.')
            sys.exit(1)

        return experiment_group
