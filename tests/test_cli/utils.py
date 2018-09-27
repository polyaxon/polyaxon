# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from unittest import TestCase

from click.testing import CliRunner


class BaseCommandTestCase(TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.mock_config()

    def mock_config(self):
        patcher = patch('polyaxon_cli.managers.config.GlobalConfigManager.get_value')
        patcher.start()
        self.addCleanup(patcher.stop)
