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

import atexit
import sys
import time

from polyaxon_sdk import V1Agent
from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon import settings
from polyaxon.agents.base import BaseAgent
from polyaxon.lifecycle import V1StatusCondition, V1Statuses
from polyaxon.logger import logger


class Agent(BaseAgent):
    def __init__(self, owner, agent_uuid):
        super().__init__(sleep_interval=None)

        self.owner = owner
        self.agent_uuid = agent_uuid
        self._register()

    def _register(self):
        logger.info("Agent is starting.")
        try:
            agent_state = self.get_state()
            if agent_state.status == V1Statuses.STOPPED:
                logger.info(
                    "Agent has been stopped from the platform,"
                    "but the deployment is still running."
                    "Please either set the agent to starting or teardown the agent deployment."
                )
                return
            self.sync()
            self.log_agent_running()
        except (ApiException, HTTPError) as e:
            self.log_agent_failed(
                message="Could not start the agent {}.".format(repr(e))
            )
            sys.exit(1)
        atexit.register(self._wait)

    def _wait(self):
        if not self._graceful_shutdown:
            self.log_agent_warning()
        time.sleep(1)

    def get_state(self):
        return self.client.agents_v1.get_agent_state(
            owner=self.owner, uuid=self.agent_uuid
        )

    def log_agent_status(self, status: str, reason: str = None, message: str = None):
        status_condition = V1StatusCondition.get_condition(
            type=status, status=True, reason=reason, message=message
        )
        self.client.agents_v1.create_agent_status(
            owner=self.owner,
            uuid=self.agent_uuid,
            body={"condition": status_condition},
            async_req=True,
        )

    def sync(self):
        self.client.agents_v1.sync_agent(
            owner=self.owner,
            agent_uuid=self.agent_uuid,
            body=V1Agent(content=settings.AGENT_CONFIG.to_dict(dump=True)),
        )

    def log_agent_running(self):
        self.log_agent_status(status=V1Statuses.RUNNING, reason="PolyaxonAgentRunning")

    def log_agent_failed(self, message=None):
        self.log_agent_status(
            status=V1Statuses.FAILED, reason="PolyaxonAgentFailed", message=message
        )

    def log_agent_warning(self):
        self.log_agent_status(
            status=V1Statuses.WARNING,
            reason="PolyaxonAgentWarning",
            message="The agent was interrupted, please check your deployment.",
        )
