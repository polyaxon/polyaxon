# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon_cli.managers.base import BaseConfigManager
from polyaxon_cli.utils.formatting import Printer
from polyaxon_schemas.experiment import ExperimentConfig


class ExperimentManager(BaseConfigManager):
    """Manages experiment configuration .polyaxonxp file."""

    IS_GLOBAL = False
    IS_POLYAXON_DIR = True
    CONFIG_FILE_NAME = '.polyaxonxp'
    CONFIG = ExperimentConfig

    @classmethod
    def get_config_or_raise(cls):
        experiment = cls.get_config()
        if not experiment:
            Printer.print_error('No experiment id was provided.')
            sys.exit(1)

        return experiment
