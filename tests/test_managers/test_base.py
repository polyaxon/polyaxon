# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

from mock import patch

from polyaxon_cli.managers.base import BaseConfigManager


class TestBaseConfigManger(TestCase):
    def test_default_props(self):
        assert BaseConfigManager.IS_GLOBAL is False
        assert BaseConfigManager.IS_POLYAXON_DIR is False
        assert BaseConfigManager.CONFIG_FILE_NAME is None
        assert BaseConfigManager.CONFIG is None

    @patch('polyaxon_cli.managers.base.os.path.expanduser')
    def test_get_config_file_path(self, expanduser):
        expanduser.return_value = '/tmp/'
        BaseConfigManager.CONFIG_FILE_NAME = 'testing'

        # Test configuration
        # Set IS_GLOBAL = True
        BaseConfigManager.IS_GLOBAL = False
        # Set IS_POLYAXON_DIR = True
        BaseConfigManager.IS_POLYAXON_DIR = True
        with patch.object(BaseConfigManager, '_create_dir') as path_fct:
            config_file1 = BaseConfigManager.get_config_file_path(create=True)
        assert path_fct.call_count == 1

        with patch.object(BaseConfigManager, '_create_dir') as path_fct:
            config_file2 = BaseConfigManager.get_config_file_path(create=False)
        assert path_fct.call_count == 0
        assert config_file1 == config_file2
        assert config_file1 == os.path.join('.', '.polyaxon', 'testing')

        # Test configuration
        # Set IS_POLYAXON_DIR = True
        BaseConfigManager.IS_POLYAXON_DIR = False
        with patch.object(BaseConfigManager, '_create_dir') as path_fct:
            config_file1 = BaseConfigManager.get_config_file_path(create=True)
        assert path_fct.call_count == 0

        with patch.object(BaseConfigManager, '_create_dir') as path_fct:
            config_file2 = BaseConfigManager.get_config_file_path(create=False)
        assert path_fct.call_count == 0
        assert config_file1 == config_file2
        assert config_file1 == os.path.join('.', 'testing')

        # Test configuration
        # Set IS_GLOBAL = True
        BaseConfigManager.IS_GLOBAL = True

        with patch.object(BaseConfigManager, '_create_dir') as path_fct:
            config_file1 = BaseConfigManager.get_config_file_path(create=True)
        assert path_fct.call_count == 1

        with patch.object(BaseConfigManager, '_create_dir') as path_fct:
            config_file2 = BaseConfigManager.get_config_file_path(create=False)
        assert path_fct.call_count == 0
        assert config_file1 == config_file2
        assert config_file1 == os.path.join('/tmp/', '.polyaxon', 'testing')

    def test_is_initialized(self):
        with patch.object(BaseConfigManager, 'get_config_file_path') as path_fct1:
            with patch('polyaxon_cli.managers.base.os.path.isfile') as path_fct2:
                BaseConfigManager.is_initialized()

        assert path_fct1.call_count == 1
        assert path_fct1.call_args_list[0][0] == (False,)
        assert path_fct2.call_count == 1
