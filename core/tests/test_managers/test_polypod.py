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

from polyaxon.managers.agent import AgentManager
from polyaxon.schemas.cli.agent_config import AgentConfig


@pytest.mark.managers_mark
class TestAgentConfigManager(BaseTestCase):
    def test_default_props(self):
        assert AgentManager.IS_GLOBAL is True
        assert AgentManager.CONFIG_PATH is None
        assert AgentManager.IS_POLYAXON_DIR is False
        assert AgentManager.CONFIG_FILE_NAME == ".agent"
        assert AgentManager.CONFIG == AgentConfig
