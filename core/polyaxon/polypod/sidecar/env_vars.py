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

from typing import List

from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_ARTIFACTS_STORE_NAME,
    POLYAXON_KEYS_CONTAINER_ID,
)
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common.env_vars import get_env_var
from polyaxon.utils.list_utils import to_list


def get_sidecar_env_vars(
    env_vars: List[k8s_schemas.V1EnvVar], container_id: str, artifacts_store_name: str,
) -> List[k8s_schemas.V1EnvVar]:

    env_vars = to_list(env_vars, check_none=True)[:]
    env_vars.append(get_env_var(name=POLYAXON_KEYS_CONTAINER_ID, value=container_id))
    env_vars.append(
        get_env_var(name=POLYAXON_KEYS_ARTIFACTS_STORE_NAME, value=artifacts_store_name)
    )
    return env_vars
