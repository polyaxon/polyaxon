#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

from polyaxon.schemas.cli.cli_config import CliConfig
from tests.utils import BaseTestCase


@pytest.mark.schemas_mark
class TestCliConfig(BaseTestCase):
    def test_cli_config(self):
        config_dict = {
            "current_version": "0.0.1",
            "installation": {"key": "uuid", "version": "1.1.4-rc11", "dist": "foo"},
            "compatibility": {"cli": {"min": "0.0.4", "latest": "1.1.4"}},
            "log_handler": None,
        }
        config = CliConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        config_to_dict.pop("last_check")
        assert config_to_dict == config_dict
        assert config.INTERVAL == 30 * 60
