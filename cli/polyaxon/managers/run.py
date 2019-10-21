# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon_sdk import V1Run

from polyaxon.managers.base import BaseConfigManager
from polyaxon.utils.formatting import Printer


class RunManager(BaseConfigManager):
    """Manages run configuration .polyaxonrun file."""

    IS_GLOBAL = False
    IS_POLYAXON_DIR = True
    CONFIG_FILE_NAME = ".polyaxonrun"
    CONFIG = V1Run

    @classmethod
    def get_config_or_raise(cls):
        run = cls.get_config()
        if not run:
            Printer.print_error("No run was provided.")
            sys.exit(1)

        return run
