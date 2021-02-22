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

from polyaxon.env_vars.getters.agent import get_agent_info, get_artifacts_store_name
from polyaxon.env_vars.getters.owner_entity import get_entity_full_name, get_entity_info
from polyaxon.env_vars.getters.project import (
    get_project_error_message,
    get_project_or_local,
)
from polyaxon.env_vars.getters.run import (
    get_collect_artifacts,
    get_collect_resources,
    get_log_level,
    get_project_run_or_local,
    get_run_info,
    get_run_or_local,
)
from polyaxon.env_vars.getters.versioned_entity import (
    get_component_info,
    get_model_info,
    get_versioned_entity_full_name,
    get_versioned_entity_info,
)
