# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from tests.test_cli.utils import BaseCommandTestCase

from polyaxon_cli.cli.config import config


class TestConfigManager(BaseCommandTestCase):
    @patch('polyaxon_cli.managers.config.GlobalConfigManager.get_config')
    def test_config_list(self, get_user):
        self.runner.invoke(config, ['--list'])
        assert get_user.call_count == 1
