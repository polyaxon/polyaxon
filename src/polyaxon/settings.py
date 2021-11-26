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

import os

from marshmallow import ValidationError

from polyaxon.api import LOCALHOST
from polyaxon.env_vars.keys import POLYAXON_KEYS_NO_CONFIG, POLYAXON_KEYS_SET_AGENT
from polyaxon.managers.client import ClientConfigManager
from polyaxon.managers.user import UserConfigManager
from polyaxon.utils.bool_utils import to_bool
from polyaxon.utils.formatting import Printer

MIN_TIMEOUT = 1
LONG_REQUEST_TIMEOUT = 3600
HEALTH_CHECK_INTERVAL = 60

AUTH_CONFIG = None
CLIENT_CONFIG = None
CLI_CONFIG = None
PROXIES_CONFIG = None
AGENT_CONFIG = None


def set_proxies_config():
    from polyaxon.managers.proxies import ProxiesManager

    global PROXIES_CONFIG

    PROXIES_CONFIG = ProxiesManager.get_config_from_env()


def set_agent_config():
    from polyaxon.managers.agent import AgentConfigManager

    global AGENT_CONFIG

    AGENT_CONFIG = AgentConfigManager.get_config_from_env()


def set_cli_config():
    from polyaxon.managers.cli import CliConfigManager

    global CLI_CONFIG

    try:
        CLI_CONFIG = CliConfigManager.get_config_or_default()
    except (TypeError, ValidationError):
        CliConfigManager.purge()
        Printer.print_warning("Your CLI Configuration was purged!")


def set_client_config():
    global CLIENT_CONFIG

    try:
        CLIENT_CONFIG = ClientConfigManager.get_config_from_env()
    except (TypeError, ValidationError):
        ClientConfigManager.purge()
        Printer.print_warning("Your client Configuration was purged!")
        CLIENT_CONFIG = ClientConfigManager.get_config_from_env()


def set_auth_config():
    from polyaxon.managers.auth import AuthConfigManager

    global AUTH_CONFIG
    try:
        AUTH_CONFIG = AuthConfigManager.get_config_from_env()
    except (TypeError, ValidationError):
        AuthConfigManager.purge()
        Printer.print_warning("Your auth Configuration was purged!")

    try:
        UserConfigManager.get_config_or_default()
    except (TypeError, ValidationError):
        UserConfigManager.purge()
        Printer.print_warning("Your user Configuration was purged!")


if not to_bool(os.environ.get(POLYAXON_KEYS_NO_CONFIG, False)):
    set_auth_config()
    set_client_config()
    if to_bool(os.environ.get(POLYAXON_KEYS_SET_AGENT, False)):
        set_agent_config()
else:
    CLIENT_CONFIG = ClientConfigManager.CONFIG(host=LOCALHOST)
