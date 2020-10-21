#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pytest

from mock import patch

from polyaxon.managers.base import BaseConfigManager
from tests.utils import BaseTestCase


@pytest.mark.managers_mark
class TestBaseConfigManger(BaseTestCase):
    class DummyConfigManger(BaseConfigManager):
        pass

    def test_default_props(self):
        assert self.DummyConfigManger.is_global() is False
        assert self.DummyConfigManger.is_local() is False
        assert self.DummyConfigManger.is_all_visibility() is False
        assert self.DummyConfigManger.is_path_visibility() is False
        assert self.DummyConfigManger.IS_POLYAXON_DIR is False
        assert self.DummyConfigManger.CONFIG_FILE_NAME is None
        assert self.DummyConfigManger.CONFIG is None

    @patch("polyaxon.managers.base.os.path.expanduser")
    def test_get_config_filepath(self, expanduser):
        expanduser.return_value = "/tmp/"
        self.DummyConfigManger.CONFIG_FILE_NAME = "testing"

        # Test configuration
        # Set IS_GLOBAL = False
        self.DummyConfigManger.VISIBILITY = BaseConfigManager.VISIBILITY_LOCAL
        # Set IS_POLYAXON_DIR = True
        self.DummyConfigManger.IS_POLYAXON_DIR = True
        with patch.object(self.DummyConfigManger, "_create_dir") as path_fct:
            config_file1 = self.DummyConfigManger.get_config_filepath(create=True)
        assert path_fct.call_count == 1

        with patch.object(self.DummyConfigManger, "_create_dir") as path_fct:
            config_file2 = self.DummyConfigManger.get_config_filepath(create=False)
        assert path_fct.call_count == 0
        assert config_file1 == config_file2
        assert config_file1 == os.path.join(".", ".polyaxon", "testing")

        # Test configuration
        # Set IS_POLYAXON_DIR = True
        self.DummyConfigManger.IS_POLYAXON_DIR = False
        with patch.object(self.DummyConfigManger, "_create_dir") as path_fct:
            config_file1 = self.DummyConfigManger.get_config_filepath(create=True)
        assert path_fct.call_count == 0

        with patch.object(self.DummyConfigManger, "_create_dir") as path_fct:
            config_file2 = self.DummyConfigManger.get_config_filepath(create=False)
        assert path_fct.call_count == 0
        assert config_file1 == config_file2
        assert config_file1 == os.path.join(".", "testing")

        # Test configuration
        # Set IS_GLOBAL = True
        self.DummyConfigManger.VISIBILITY = BaseConfigManager.VISIBILITY_GLOBAL

        with patch.object(self.DummyConfigManger, "_create_dir") as path_fct:
            config_file1 = self.DummyConfigManger.get_config_filepath(create=True)
        assert path_fct.call_count == 1

        with patch.object(self.DummyConfigManger, "_create_dir") as path_fct:
            config_file2 = self.DummyConfigManger.get_config_filepath(create=False)
        assert path_fct.call_count == 0
        assert config_file1 == config_file2
        assert config_file1 == os.path.join("/tmp/", ".polyaxon", "testing")

    def test_is_initialized(self):
        with patch.object(self.DummyConfigManger, "get_config_filepath") as path_fct1:
            with patch("polyaxon.managers.base.os.path.isfile") as path_fct2:
                self.DummyConfigManger.is_initialized()

        assert path_fct1.call_count == 1
        assert path_fct1.call_args_list[0][0] == ()
        assert path_fct1.call_args_list[0][1] == {"create": False}
        assert path_fct2.call_count == 1
