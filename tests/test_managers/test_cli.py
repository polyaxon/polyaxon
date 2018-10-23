# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import uuid

from unittest import TestCase

from mock import patch

from polyaxon_cli.managers.cli import CliConfigManager
from polyaxon_cli.schemas.cli_configuration import CliConfigurationConfig


class TestCliConfigManager(TestCase):
    def test_default_props(self):
        assert CliConfigManager.IS_GLOBAL is True
        assert CliConfigManager.IS_POLYAXON_DIR is False
        assert CliConfigManager.CONFIG_FILE_NAME == '.polyaxoncli'
        assert CliConfigManager.CONFIG == CliConfigurationConfig
        assert CliConfigManager.FREQUENCY == 3


class TestCliConfigManagerMethods(TestCase):
    def setUp(self):
        self.filename = uuid.uuid4().hex
        CliConfigManager.CONFIG_FILE_NAME = self.filename

    def tearDown(self):
        path = CliConfigManager.get_config_file_path(create=False)
        if not os.path.exists(path):
            return
        os.remove(path)

    def test_get_count(self):
        assert CliConfigManager._get_count() == 1

    def test_set_new_count(self):
        with patch.object(CliConfigManager, 'set_config') as patch_fct:
            CliConfigManager.reset(check_count=4)

        assert patch_fct.call_count == 1

    def test_should_check(self):
        with patch.object(CliConfigManager, 'reset') as patch_fct:
            result = CliConfigManager.should_check()

        assert patch_fct.call_count == 1
        assert result is True

        CliConfigManager.reset(current_version='0.0.5', min_version='0.0.4')
        with patch.object(CliConfigManager, 'reset') as patch_fct:
            result = CliConfigManager.should_check()

        assert patch_fct.call_count == 1
        assert result is False

        CliConfigManager.reset(check_count=4, current_version='0.0.5', min_version='0.0.4')
        with patch.object(CliConfigManager, 'reset') as patch_fct:
            result = CliConfigManager.should_check()

        assert patch_fct.call_count == 1
        assert result is True

        CliConfigManager.reset(current_version='0.0.2', min_version='0.0.4')
        with patch.object(CliConfigManager, 'reset') as patch_fct:
            result = CliConfigManager.should_check()

        assert patch_fct.call_count == 1
        assert result is True
