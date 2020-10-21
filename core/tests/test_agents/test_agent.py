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

from mock import MagicMock, patch

from polyaxon.agents.agent import Agent
from polyaxon.agents.base import BaseAgent
from polyaxon.agents.spawners.spawner import Spawner
from polyaxon.client import PolyaxonClient
from tests.utils import BaseTestCase


@pytest.mark.agent_mark
class TestAgents(BaseTestCase):
    SET_AGENT_SETTINGS = True

    def test_init_base_agent(self):
        agent = BaseAgent()
        assert agent.sleep_interval is None
        assert isinstance(agent.spawner, Spawner)
        assert isinstance(agent.client, PolyaxonClient)

    @patch("polyaxon_sdk.AgentsV1Api.sync_agent")
    @patch("polyaxon_sdk.AgentsV1Api.create_agent_status")
    @patch("polyaxon_sdk.AgentsV1Api.get_agent_state")
    @patch("polyaxon_sdk.AgentsV1Api.get_agent")
    @patch("polyaxon.agents.base.Spawner")
    def test_init_agent(
        self, _, get_agent, get_agent_state, create_agent_status, sync_agent
    ):
        get_agent_state.return_value = MagicMock(status=None)
        agent = Agent(owner="foo", agent_uuid="uuid")
        assert agent.sleep_interval is None
        assert agent.spawner is not None
        assert isinstance(agent.client, PolyaxonClient)
        assert get_agent.call_count == 1
        assert get_agent_state.call_count == 0
        assert create_agent_status.call_count == 1
        assert sync_agent.call_count == 1
        assert agent.spawner.k8s_manager.get_version.call_count == 1
