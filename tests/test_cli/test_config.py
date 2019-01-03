# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon_cli.cli.config import config


class TestConfigManager(BaseCommandTestCase):
    @patch('polyaxon_cli.managers.config.GlobalConfigManager.is_initialized')
    def test_config_list_checks_initialized(self, is_initialized):
        is_initialized.return_value = False
        self.runner.invoke(config, ['--list'])
        assert is_initialized.call_count == 1

    @patch('polyaxon_cli.managers.config.GlobalConfigManager.is_initialized')
    @patch('polyaxon_cli.managers.config.GlobalConfigManager.CONFIG')
    def test_config_list_gets_default_config(self, default_config, is_initialized):
        is_initialized.return_value = False
        self.runner.invoke(config, ['--list'])
        assert default_config.call_count == 1

    @patch('polyaxon_cli.managers.config.GlobalConfigManager.is_initialized')
    @patch('polyaxon_cli.managers.config.GlobalConfigManager.get_config')
    def test_config_list_gets_file_config(self, get_config, is_initialized):
        is_initialized.return_value = True
        self.runner.invoke(config, ['--list'])
        assert get_config.call_count == 1
