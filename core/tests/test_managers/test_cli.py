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
import uuid

import pytest

from mock import patch
from tests.utils import BaseTestCase

from polyaxon.managers.cli import CliConfigManager
from polyaxon.schemas.cli.cli_config import CliConfigurationConfig


@pytest.mark.managers_mark
class TestCliConfigManager(BaseTestCase):
    def test_default_props(self):
        assert CliConfigManager.IS_GLOBAL is True
        assert CliConfigManager.IS_POLYAXON_DIR is False
        assert CliConfigManager.CONFIG_FILE_NAME == ".polyaxoncli"
        assert CliConfigManager.CONFIG == CliConfigurationConfig
        assert CliConfigManager.FREQUENCY == 3


@pytest.mark.managers_mark
class TestCliConfigManagerMethods(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.filename = uuid.uuid4().hex
        CliConfigManager.CONFIG_FILE_NAME = self.filename

    def tearDown(self):
        path = CliConfigManager.get_config_filepath(create=False)
        if not os.path.exists(path):
            return
        os.remove(path)

    def test_get_count(self):
        assert CliConfigManager._get_count() == 1

    def test_set_new_count(self):
        with patch.object(CliConfigManager, "set_config") as patch_fct:
            CliConfigManager.reset(check_count=4)

        assert patch_fct.call_count == 1

    def test_should_check(self):
        with patch.object(CliConfigManager, "reset") as patch_fct:
            result = CliConfigManager.should_check()

        assert patch_fct.call_count == 1
        assert result is True

        CliConfigManager.reset(
            current_version="0.0.5", server_versions={"cli": {"min_version": "0.0.4"}}
        )
        with patch.object(CliConfigManager, "reset") as patch_fct:
            result = CliConfigManager.should_check()

        assert patch_fct.call_count == 1
        assert result is False

        CliConfigManager.reset(
            check_count=4,
            current_version="0.0.5",
            server_versions={"cli": {"min_version": "0.0.4"}},
        )
        with patch.object(CliConfigManager, "reset") as patch_fct:
            result = CliConfigManager.should_check()

        assert patch_fct.call_count == 1
        assert result is True

        CliConfigManager.reset(
            current_version="0.0.2", server_versions={"cli": {"min_version": "0.0.4"}}
        )
        with patch.object(CliConfigManager, "reset") as patch_fct:
            result = CliConfigManager.should_check()

        assert patch_fct.call_count == 1
        assert result is True
