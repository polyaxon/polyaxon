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

from polyaxon.contexts import keys

INPUTS = "inputs"
OUTPUTS = "outputs"
INPUTS_OUTPUTS = "io"
ARTIFACTS = "artifacts"
GLOBALS = "globals"

CONTEXTS = {
    INPUTS,
    OUTPUTS,
    INPUTS_OUTPUTS,
    ARTIFACTS,
}
CONTEXTS_WITH_NESTING = {
    INPUTS,
    OUTPUTS,
    ARTIFACTS,
    GLOBALS,
}
GLOBALS_CONTEXTS = {
    keys.OWNER_NAME,
    keys.PROJECT_NAME,
    keys.PROJECT_UNIQUE_NAME,
    keys.PROJECT_UUID,
    keys.RUN_INFO,
    keys.NAME,
    keys.UUID,
    keys.STATUS,
    keys.NAMESPACE,
    keys.ITERATION,
    keys.CONTEXT_PATH,
    keys.ARTIFACTS_PATH,
    keys.CREATED_AT,
    keys.COMPILED_AT,
    keys.SCHEDULE_AT,
    keys.STARTED_AT,
    keys.FINISHED_AT,
    keys.DURATION,
    keys.CLONING_KIND,
    keys.ORIGINAL_UUID,
    keys.IS_INDEPENDENT,
}
