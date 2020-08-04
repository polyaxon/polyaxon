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

from polyaxon.polyflow import ForConfig, IfConfig


class Sections:
    VERSION = "version"
    KIND = "kind"
    NAME = "name"
    DESCRIPTION = "description"
    TAGS = "tags"
    PROFILE = "profile"
    QUEUE = "queue"
    CACHE = "cache"
    PLUGINS = "plugins"
    TERMINATION = "termination"
    INPUTS = "inputs"
    OUTPUTS = "outputs"
    PARAMS = "params"
    CONNECTIONS = "connections"
    RUN = "run"
    RUN_PATCH = "runPatch"
    MATRIX = "matrix"
    OPERATIONS = "operations"
    COMPONENTS = "components"
    SCHEDULE = "schedule"
    DEPENDENCIES = "dependencies"
    TRIGGER = "trigger"
    CONDITIONS = "conditions"
    SKIP_ON_UPSTREAM_SKIP = "skipOnUpstreamSkip"
    HUB_REF = "hubRef"
    DAG_REF = "dagRef"
    PATH_REF = "pathRef"
    URL_REF = "urlRef"
    COMPONENT = "component"

    SECTIONS = (
        VERSION,
        KIND,
        NAME,
        DESCRIPTION,
        TAGS,
        PARAMS,
        PROFILE,
        CACHE,
        PLUGINS,
        TERMINATION,
        CONNECTIONS,
        MATRIX,
        OPERATIONS,
        SCHEDULE,
        DEPENDENCIES,
        TRIGGER,
        CONDITIONS,
        SKIP_ON_UPSTREAM_SKIP,
        HUB_REF,
        DAG_REF,
        PATH_REF,
        URL_REF,
        COMPONENT,
        INPUTS,
        OUTPUTS,
        RUN,
        RUN_PATCH,
    )

    PARSING_SECTIONS = (PROFILE, QUEUE, CACHE, CONNECTIONS, PLUGINS, TERMINATION)
    OP_PARSING_SECTIONS = (OPERATIONS, SCHEDULE, DEPENDENCIES, TRIGGER, CONDITIONS)

    REQUIRED_SECTIONS = (VERSION, KIND)

    OPERATORS = {ForConfig.IDENTIFIER: ForConfig, IfConfig.IDENTIFIER: IfConfig}
