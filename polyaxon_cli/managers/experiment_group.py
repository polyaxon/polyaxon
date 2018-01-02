# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon_schemas.experiment import ExperimentConfig

from polyaxon_cli.managers.base import BaseConfigManager
from polyaxon_cli.utils.formatting import Printer


class ExperimentManager(BaseConfigManager):
    """Manages experiment configuration .polyaxonxpgroup file."""

    IS_GLOBAL = False
    IS_POLYAXON_DIR = True
    CONFIG_FILE_NAME = '.polyaxonxpgroup'
    CONFIG = ExperimentConfig

    @classmethod
    def get_config_or_raise(cls):
        experiment_group = cls.get_config()
        if not experiment_group:
            Printer.print_error('No experiment_group sequence was provided.')
            sys.exit(1)

        return experiment_group
