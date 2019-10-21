# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon.managers.base import BaseConfigManager
from polyaxon.schemas.cli.client_configuration import ClientConfig


class ClientConfigManager(BaseConfigManager):
    """Manages client configuration .polyaxonclient file."""

    IS_GLOBAL = True
    CONFIG_FILE_NAME = ".polyaxonclient"
    CONFIG = ClientConfig
