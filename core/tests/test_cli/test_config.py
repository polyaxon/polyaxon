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
