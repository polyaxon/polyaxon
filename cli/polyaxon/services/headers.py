#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8


POLYAXON_HEADERS_CLI_VERSION = "X_POLYAXON_CLI_VERSION"
POLYAXON_HEADERS_CLIENT_VERSION = "X_POLYAXON_CLIENT_VERSION"
POLYAXON_HEADERS_INTERNAL = "X_POLYAXON_INTERNAL"
POLYAXON_HEADERS_SERVICE = "X_POLYAXON_SERVICE"


class PolyaxonServices(object):  # noqa
    INITIALIZER = "initializer"
    SIDECAR = "sidecar"
    RUNNER = "runner"
    AGENT = "agent"

    VALUES = {INITIALIZER, SIDECAR, RUNNER, AGENT}
