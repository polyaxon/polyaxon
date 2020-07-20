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
from polyaxon.env_vars.getters.agent import get_agent_info
from polyaxon.env_vars.getters.component import (
    get_component_full_name,
    get_component_info,
)
from polyaxon.env_vars.getters.project import (
    get_project_full_name,
    get_project_info,
    get_project_or_local,
)
from polyaxon.env_vars.getters.run import (
    get_collect_artifact,
    get_collect_resources,
    get_log_level,
    get_project_run_or_local,
    get_run_info,
    get_run_or_local,
)
