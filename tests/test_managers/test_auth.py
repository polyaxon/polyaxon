# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_cli.managers.auth import AuthConfigManager
from polyaxon_schemas.authentication import AccessTokenConfig


class TestAuthConfigManager(TestCase):
    def test_default_props(self):
        assert AuthConfigManager.IS_GLOBAL is True
        assert AuthConfigManager.IS_POLYAXON_DIR is False
        assert AuthConfigManager.CONFIG_FILE_NAME == '.polyaxonauth'
        assert AuthConfigManager.CONFIG == AccessTokenConfig
