# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_cli.managers.base import BaseConfigManager
from polyaxon_cli.schemas.global_configuration import GlobalConfigurationConfig


class GlobalConfigManager(BaseConfigManager):
    """Manages global configuration .polyaxonconfig file."""

    IS_GLOBAL = True
    CONFIG_FILE_NAME = '.polyaxonconfig'
    CONFIG = GlobalConfigurationConfig
