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

from polyaxon.auxiliaries import V1PolyaxonInitContainer
from polyaxon.containers.contexts import CONTEXT_MOUNT_ARTIFACTS
from polyaxon.containers.names import INIT_GIT_CONTAINER_PREFIX, generate_container_name
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


def get_repo_context_args(
    name: str, url: str, revision: str, mount_path: str, connection: str = None
) -> List[str]:
    if not name:
        raise PolypodException("A repo name is required to create a repo context.")
    if not url:
        raise PolypodException("A repo url is required to create a repo context.")

    args = ["--repo-path={}/{}".format(mount_path, name), "--url={}".format(url)]

    if revision:
        args.append("--revision={}".format(revision))

    if connection:
        args.append("--connection={}".format(connection))
    return args


def get_git_init_container(
    polyaxon_init: V1PolyaxonInitContainer,
    connection: V1ConnectionType,
    contexts: PluginsContextsSpec,
    container: Optional[k8s_schemas.V1Container] = None,
    env: List[k8s_schemas.V1EnvVar] = None,
    mount_path: str = None,
    track: bool = False,
) -> k8s_schemas.V1Container:
    if not connection:
        raise PolypodException("A connection is required to create a repo context.")
    if not container:
        container = k8s_schemas.V1Container(
            name=generate_container_name(INIT_GIT_CONTAINER_PREFIX, connection.name),
        )

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
    args = get_repo_context_args(
        name=connection.name,
        url=connection.schema.url,
        revision=connection.schema.revision,
        mount_path=mount_path,
        connection=connection.name if track else None,
    )
    return patch_container(
        container=container,
        name=generate_container_name(INIT_GIT_CONTAINER_PREFIX, connection.name),
        image=polyaxon_init.get_image(),
        image_pull_policy=polyaxon_init.image_pull_policy,
        command=["polyaxon", "initializer", "git"],
        args=args,
        env=env,
        env_from=env_from,
        volume_mounts=volume_mounts,
        resources=polyaxon_init.get_resources(),
    )
