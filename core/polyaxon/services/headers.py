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


class PolyaxonServiceHeaders:
    CLI_VERSION = "X_POLYAXON_CLI_VERSION"
    CLIENT_VERSION = "X_POLYAXON_CLIENT_VERSION"
    INTERNAL = "X_POLYAXON_INTERNAL"
    SERVICE = "X_POLYAXON_SERVICE"

    @staticmethod
    def get_header(header):
        return header.replace("_", "-")


class PolyaxonServices:  # noqa
    PLATFORM = "platform"
    AUTH = "auth"
    UI = "ui"
    CLI = "cli"
    INITIALIZER = "initializer"
    SIDECAR = "sidecar"
    RUNNER = "runner"
    AGENT = "agent"
    OPERATOR = "operator"
    BILLING = "billing"

    VALUES = {
        PLATFORM,
        CLI,
        UI,
        AUTH,
        INITIALIZER,
        SIDECAR,
        RUNNER,
        AGENT,
        OPERATOR,
        BILLING,
    }
    AGENT_VALUES = [PLATFORM, CLI, UI, OPERATOR, AGENT, INITIALIZER, SIDECAR]
