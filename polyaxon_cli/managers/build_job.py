# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon_cli.managers.base import BaseConfigManager
from polyaxon_cli.schemas import BuildJobConfig
from polyaxon_cli.utils.formatting import Printer


class BuildJobManager(BaseConfigManager):
    """Manages build job configuration .polyaxonbuild file."""

    IS_GLOBAL = False
    IS_POLYAXON_DIR = True
    CONFIG_FILE_NAME = '.polyaxonbuild'
    CONFIG = BuildJobConfig

    @classmethod
    def get_config_or_raise(cls):
        job = cls.get_config()
        if not job:
            Printer.print_error('No build job uuid was provided.')
            sys.exit(1)

        return job
