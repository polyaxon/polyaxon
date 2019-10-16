# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon.managers.base import BaseConfigManager
from polyaxon.schemas.cli.client_configuration import GlobalConfigurationConfig


class GlobalConfigManager(BaseConfigManager):
    """Manages global configuration .polyaxonconfig file."""

    IS_GLOBAL = True
    CONFIG_FILE_NAME = ".polyaxonconfig"
    CONFIG = GlobalConfigurationConfig
