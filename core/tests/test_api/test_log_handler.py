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

from tests.utils import BaseTestCase

from polyaxon.schemas.api.log_handler import LogHandlerConfig


@pytest.mark.api_mark
class TestLogHandlerConfig(BaseTestCase):
    def test_log_handler_config(self):
        config_dict = {"dsn": "https//foo:bar", "environment": "staging"}
        config = LogHandlerConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
