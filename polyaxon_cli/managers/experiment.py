# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.experiment import ExperimentConfig

from polyaxon_cli.managers.base import BaseConfigManager


class ExperimentManager(BaseConfigManager):
    """Manages experiment configuration .polyaxonxp file."""

    IS_GLOBAL = False
    IS_POLYAXON_DIR = True
    CONFIG_FILE_NAME = '.polyaxonxp'
    CONFIG = ExperimentConfig
