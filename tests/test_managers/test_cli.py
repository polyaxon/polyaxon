# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from unittest import TestCase

from polyaxon_cli.managers.cli import CliConfigManager
from polyaxon_cli.schemas.cli_configuration import CliConfigurationConfig


class TestCliConfigManager(TestCase):
    def test_default_props(self):
        assert CliConfigManager.IS_GLOBAL is True
        assert CliConfigManager.IS_POLYAXON_DIR is False
        assert CliConfigManager.CONFIG_FILE_NAME == '.polyaxoncli'
        assert CliConfigManager.CONFIG == CliConfigurationConfig
        assert CliConfigManager.FREQUENCY == 5

    def test_get_count(self):
        assert CliConfigManager._get_count() == 1

    def test_set_new_count(self):
        with patch.object(CliConfigManager, 'set_config') as patch_fct:
            CliConfigManager._set_new_count(4)

        assert patch_fct.call_count == 1

    def test_should_check(self):
        with patch.object(CliConfigManager, '_set_new_count') as patch_fct:
            result = CliConfigManager.should_check()

        assert patch_fct.call_count == 1
        assert result is False
