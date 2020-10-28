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

from typing import List, Optional

from polyaxon.containers.contexts import CONTEXT_MOUNT_ARTIFACTS
from polyaxon.containers.names import (
    INIT_CUSTOM_CONTAINER_PREFIX,
    generate_container_name,
)
from polyaxon.exceptions import PolypodException
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common import constants
from polyaxon.polypod.common.containers import patch_container
from polyaxon.polypod.common.env_vars import (
    get_connection_env_var,
    get_env_from_config_map,
    get_env_from_secret,
    get_items_from_config_map,
    get_items_from_secret,
)
from polyaxon.polypod.common.mounts import (
    get_auth_context_mount,
    get_connections_context_mount,
    get_mount_from_resource,
)
from polyaxon.polypod.common.volumes import get_volume_name
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1ConnectionType
from polyaxon.utils.list_utils import to_list


def get_custom_init_container(
    connection: V1ConnectionType,
    contexts: PluginsContextsSpec,
    container: Optional[k8s_schemas.V1Container],
    env: List[k8s_schemas.V1EnvVar] = None,
    mount_path: str = None,
) -> k8s_schemas.V1Container:
    if not connection:
        raise PolypodException("A connection is required to create a repo context.")

    volume_name = (
        get_volume_name(mount_path)
        if mount_path
        else constants.CONTEXT_VOLUME_ARTIFACTS
    )
    mount_path = mount_path or CONTEXT_MOUNT_ARTIFACTS
    volume_mounts = [
        get_connections_context_mount(name=volume_name, mount_path=mount_path)
    ]

    if contexts and contexts.auth:
        volume_mounts.append(get_auth_context_mount(read_only=True))

    env = to_list(env, check_none=True)
    env_from = []
    secret = connection.get_secret()
    if secret:
        volume_mounts += to_list(
            get_mount_from_resource(resource=secret), check_none=True
        )
        env += to_list(get_items_from_secret(secret=secret), check_none=True)
        env_from = to_list(get_env_from_secret(secret=secret), check_none=True)
    env += to_list(
        get_connection_env_var(connection=connection, secret=secret), check_none=True
    )
    config_map = connection.get_config_map()
    if config_map:
        volume_mounts += to_list(
            get_mount_from_resource(resource=config_map), check_none=True
        )
        env += to_list(
            get_items_from_config_map(config_map=config_map), check_none=True
        )
        env_from = to_list(
            get_env_from_config_map(config_map=config_map), check_none=True
        )
    container_name = container.name or generate_container_name(
        INIT_CUSTOM_CONTAINER_PREFIX, connection.name
    )
    return patch_container(
        container=container,
        name=container_name,
        env=env,
        env_from=env_from,
        volume_mounts=volume_mounts,
    )
