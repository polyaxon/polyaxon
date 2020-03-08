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

from typing import Iterable, List

from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_COLLECT_ARTIFACTS,
    POLYAXON_KEYS_COLLECT_RESOURCES,
    POLYAXON_KEYS_LOG_LEVEL,
)
from polyaxon.exceptions import PolyaxonSchemaError, PolypodException
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common.env_vars import (
    get_connection_env_var,
    get_env_var,
    get_env_vars_from_k8s_resources,
    get_kv_env_vars,
)
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType
from polyaxon.utils.list_utils import to_list


def get_env_vars(
    contexts: PluginsContextsSpec,
    log_level: str,
    kv_env_vars: List[List],
    connections: Iterable[V1ConnectionType],
    secrets: Iterable[V1K8sResourceType],
    config_maps: Iterable[V1K8sResourceType],
) -> List[k8s_schemas.V1EnvVar]:
    env_vars = []
    connections = connections or []

    if log_level:
        env_vars.append(get_env_var(name=POLYAXON_KEYS_LOG_LEVEL, value=log_level))

    if contexts and contexts.collect_artifacts:
        env_vars.append(get_env_var(name=POLYAXON_KEYS_COLLECT_ARTIFACTS, value=True))

    if contexts and contexts.collect_resources:
        env_vars.append(get_env_var(name=POLYAXON_KEYS_COLLECT_RESOURCES, value=True))

    # Add connection env vars information
    for connection in connections:
        try:
            secret = connection.get_secret()
            env_vars += to_list(
                get_connection_env_var(connection=connection, secret=secret),
                check_none=True,
            )
        except PolyaxonSchemaError as e:
            raise PolypodException("Error resolving secrets: %s" % e) from e

    env_vars += get_kv_env_vars(kv_env_vars)
    env_vars += get_env_vars_from_k8s_resources(
        secrets=secrets, config_maps=config_maps
    )
    return env_vars
