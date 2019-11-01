# coding: utf-8
from __future__ import absolute_import, division, print_function

import pytest

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon.cli.config import config


@pytest.mark.cli_mark
class TestCliConfig(BaseCommandTestCase):
    @patch("polyaxon.managers.client.ClientConfigManager.is_initialized")
    def test_config_list_checks_initialized(self, is_initialized):
        is_initialized.return_value = False
        self.runner.invoke(config, ["--list"])
        assert is_initialized.call_count == 1

    @patch("polyaxon.managers.client.ClientConfigManager.is_initialized")
    @patch("polyaxon.managers.client.ClientConfigManager.CONFIG")
    def test_config_list_gets_default_config(self, default_config, is_initialized):
        is_initialized.return_value = False
        self.runner.invoke(config, ["--list"])
        assert default_config.call_count == 1

    @patch("polyaxon.managers.client.ClientConfigManager.is_initialized")
    @patch("polyaxon.managers.client.ClientConfigManager.get_config")
    def test_config_list_gets_file_config(self, get_config, is_initialized):
        is_initialized.return_value = True
        self.runner.invoke(config, ["--list"])
        assert get_config.call_count == 1
