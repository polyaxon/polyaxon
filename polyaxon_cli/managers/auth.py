# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.access_token import AccessTokenConfig
from polyaxon_cli.managers.base import BaseConfigManager


class AuthConfigManager(BaseConfigManager):
    """Manages access token configuration .plxauthconfig file."""

    IS_GLOBAL = True
    CONFIG_FILE_NAME = '.plxauthconfig'
    CONFIG = AccessTokenConfig
    INIT_COMMAND = True
