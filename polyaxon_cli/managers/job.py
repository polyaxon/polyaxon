# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon_cli.managers.base import BaseConfigManager
from polyaxon_cli.utils.formatting import Printer
from polyaxon_schemas.job import JobConfig


class JobManager(BaseConfigManager):
    """Manages job configuration .polyaxonjob file."""

    IS_GLOBAL = False
    IS_POLYAXON_DIR = True
    CONFIG_FILE_NAME = '.polyaxonjob'
    CONFIG = JobConfig

    @classmethod
    def get_config_or_raise(cls):
        job = cls.get_config()
        if not job:
            Printer.print_error('No job uuid was provided.')
            sys.exit(1)

        return job
