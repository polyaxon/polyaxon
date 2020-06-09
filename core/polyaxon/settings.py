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

from polyaxon.managers.auth import AuthConfigManager
from polyaxon.managers.client import ClientConfigManager
from polyaxon.utils.bool_utils import to_bool

MIN_TIMEOUT = 1
LONG_REQUEST_TIMEOUT = 3600
HEALTH_CHECK_INTERVAL = 60

AUTH_CONFIG = None
CLIENT_CONFIG = None
PROXIES_CONFIG = None
AGENT_CONFIG = None

if not to_bool(os.environ.get("POLYAXON_NO_CONFIG", False)):
    AUTH_CONFIG = AuthConfigManager.get_config_from_env()
    CLIENT_CONFIG = ClientConfigManager.get_config_from_env()

    if CLIENT_CONFIG.set_agent:
        from polyaxon.managers.agent import AgentManager

        AGENT_CONFIG = AgentManager.get_config_from_env(
            agent_path=CLIENT_CONFIG.agent_path
        )
else:
    CLIENT_CONFIG = ClientConfigManager.CONFIG()


def set_proxies_config():
    from polyaxon.managers.proxies import ProxiesManager

    global PROXIES_CONFIG

    PROXIES_CONFIG = ProxiesManager.get_config_from_env()
