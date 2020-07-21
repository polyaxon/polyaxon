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

from datetime import timedelta

import pytest

from mock import patch
from tests.utils import BaseTestCase

from polyaxon.managers.cli import CliConfigManager
from polyaxon.schemas.cli.cli_config import CliConfig
from polyaxon.utils.tz_utils import now


@pytest.mark.managers_mark
class TestCliConfigManager(BaseTestCase):
    def test_default_props(self):
        assert CliConfigManager.is_global() is True
        assert CliConfigManager.IS_POLYAXON_DIR is False
        assert CliConfigManager.CONFIG_FILE_NAME == ".cli"
        assert CliConfigManager.CONFIG == CliConfig


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

    def test_set_compatibility(self):
        with patch.object(CliConfigManager, "set_config") as patch_fct:
            CliConfigManager.reset(current_version=True)

        assert patch_fct.call_count == 1

    def test_should_check(self):
        with patch.object(CliConfigManager, "reset") as patch_fct:
            result = CliConfigManager.should_check()

        assert patch_fct.call_count == 1
        assert result is True

        CliConfigManager.reset(
            last_check=now(),
            current_version="0.0.5",
            installation={"key": "uuid", "version": "1.1.4-rc11", "dist": "foo"},
            compatibility={"cli": {"min": "0.0.4", "latest": "1.1.4"}},
        )
        with patch.object(CliConfigManager, "reset") as patch_fct:
            result = CliConfigManager.should_check()

        assert patch_fct.call_count == 0
        assert result is False

        CliConfigManager.reset(
            last_check=now() - timedelta(seconds=10000),
            current_version="0.0.5",
            installation={"key": "uuid", "version": "1.1.4-rc11", "dist": "foo"},
            compatibility={"cli": {"min": "0.0.4", "latest": "1.1.4"}},
        )
        with patch.object(CliConfigManager, "reset") as patch_fct:
            result = CliConfigManager.should_check()

        assert patch_fct.call_count == 1
        assert result is True

        CliConfigManager.reset(
            last_check=now(),
            current_version="0.0.2",
            installation={"key": "uuid", "version": "1.1.4-rc11", "dist": "foo"},
            compatibility={"cli": {"min": "0.0.4", "latest": "1.1.4"}},
        )
        with patch.object(CliConfigManager, "reset") as patch_fct:
            result = CliConfigManager.should_check()

        # Although condition for showing a message, do not reset
        assert patch_fct.call_count == 0
        assert result is False
