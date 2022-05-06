#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from polyaxon.env_vars.keys import EV_KEYS_SERVICE


class PolyaxonServices:  # noqa
    PLATFORM = "platform"
    AUTH = "auth"
    UI = "ui"
    API = "api"
    GATEWAY = "gateway"
    STREAMS = "streams"
    SANDBOX = "sandbox"
    CLI = "cli"
    INITIALIZER = "initializer"
    INIT = "init"
    SIDECAR = "sidecar"
    RUNNER = "runner"
    AGENT = "agent"
    OPERATOR = "operator"
    BILLING = "billing"
    HP_SEARCH = "hp_search"
    EVENTS_HANDLER = "events-handlers"

    VALUES = {
        PLATFORM,
        CLI,
        UI,
        API,
        GATEWAY,
        STREAMS,
        SANDBOX,
        AUTH,
        INITIALIZER,
        SIDECAR,
        RUNNER,
        AGENT,
        OPERATOR,
        BILLING,
        HP_SEARCH,
        EVENTS_HANDLER,
    }
    AGENT_VALUES = [PLATFORM, CLI, UI, OPERATOR, AGENT, INITIALIZER, SIDECAR]
    SERVICE = None

    @classmethod
    def set_service_name(cls, value: str = None):
        cls.SERVICE = value or os.environ.get(EV_KEYS_SERVICE)

    @classmethod
    def is_agent(cls, value: str = None):
        return cls.AGENT == (value or cls.SERVICE)

    @classmethod
    def is_sandbox(cls, value: str = None):
        return cls.SANDBOX == (value or cls.SERVICE)

    @classmethod
    def is_hp_search(cls, value: str = None):
        return cls.HP_SEARCH == (value or cls.SERVICE)

    @classmethod
    def is_init(cls, value: str = None):
        return (value or cls.SERVICE) in {cls.INIT, cls.INITIALIZER}

    @classmethod
    def is_sidecar(cls, value: str = None):
        return cls.SIDECAR == (value or cls.SERVICE)

    @classmethod
    def is_streams(cls, value: str = None):
        return cls.STREAMS == (value or cls.SERVICE)

    @classmethod
    def is_api(cls, value: str = None):
        return cls.API == (value or cls.SERVICE)

    @classmethod
    def is_gateway(cls, value: str = None):
        return cls.GATEWAY == (value or cls.SERVICE)

    @classmethod
    def is_events_handlers(cls, value: str = None):
        return cls.EVENTS_HANDLER == (value or cls.SERVICE)
