# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon.managers.base import BaseConfigManager
from polyaxon.schemas.api.authentication import AccessTokenConfig


class AuthConfigManager(BaseConfigManager):
    """Manages access token configuration .polyaxonauth file."""

    IS_GLOBAL = True
    CONFIG_FILE_NAME = '.polyaxonauth'
    CONFIG = AccessTokenConfig
