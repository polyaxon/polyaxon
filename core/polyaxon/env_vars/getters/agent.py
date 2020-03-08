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

from polyaxon.env_vars.keys import POLYAXON_KEYS_AGENT_INSTANCE
from polyaxon.exceptions import PolyaxonAgentError


def get_agent_info(agent_instance: str = None):
    agent_instance = agent_instance or os.getenv(POLYAXON_KEYS_AGENT_INSTANCE, None)
    if not agent_instance:
        raise PolyaxonAgentError(
            "Could get agent info, "
            "please make sure that this agent was registered in Polyaxon."
        )

    parts = agent_instance.split(".")
    if not len(parts) == 3:
        raise PolyaxonAgentError(
            "agent instance is invalid `{}`, "
            "please make sure that this agent was registered in Polyaxon.".format(
                agent_instance
            )
        )
    return parts[0], parts[-1]
