#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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
from polyaxon.containers.names import (
    INIT_TENSORBOARD_CONTAINER_PREFIX,
    generate_container_name,
)
from polyaxon.contexts import paths as ctx_paths
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common import constants
from polyaxon.polypod.common.env_vars import get_run_instance_env_var
from polyaxon.polypod.common.mounts import (
    get_auth_context_mount,
    get_connections_context_mount,
)
from polyaxon.polypod.common.volumes import get_volume_name
from polyaxon.polypod.init.store import get_base_store_container
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1ConnectionType, V1TensorboardType
from polyaxon.utils.list_utils import to_list
from polyaxon.utils.validation import validate_tags


def _get_args(tb_args: V1TensorboardType):
    args = []
    if tb_args.port:
        args.append("--port={}".format(tb_args.port))
    if tb_args.uuids:
        uuids = validate_tags(tb_args.uuids, validate_yaml=True)
        args.append("--uuids={}".format(",".join(uuids)))
    if tb_args.use_names:
        args.append("--use-names")
    if tb_args.path_prefix:
        args.append("--path-prefix={}".format(tb_args.path_prefix)),
    if tb_args.plugins:
        plugins = validate_tags(tb_args.plugins, validate_yaml=True)
        args.append("--plugins={}".format(",".join(plugins)))

    return args


def get_tensorboard_init_container(
    polyaxon_init: V1PolyaxonInitContainer,
    artifacts_store: V1ConnectionType,
    tb_args: V1TensorboardType,
    contexts: PluginsContextsSpec,
    run_instance: str,
    container: Optional[k8s_schemas.V1Container] = None,
    env: List[k8s_schemas.V1EnvVar] = None,
    mount_path: Optional[str] = None,
) -> k8s_schemas.V1Container:
    env = to_list(env, check_none=True)
    env = env + [get_run_instance_env_var(run_instance)]

    container_name = generate_container_name(INIT_TENSORBOARD_CONTAINER_PREFIX)
    if not container:
        container = k8s_schemas.V1Container(name=container_name)

    volume_name = (
        get_volume_name(mount_path) if mount_path else constants.VOLUME_MOUNT_ARTIFACTS
    )
    mount_path = mount_path or ctx_paths.CONTEXT_MOUNT_ARTIFACTS
    volume_mounts = [
        get_connections_context_mount(name=volume_name, mount_path=mount_path)
    ]
    if contexts and contexts.auth:
        volume_mounts.append(get_auth_context_mount(read_only=True))

    args = [
        "--context-from={}".format(artifacts_store.store_path),
        "--context-to={}".format(mount_path),
        "--connection-kind={}".format(artifacts_store.kind),
    ]
    args += _get_args(tb_args)

    return get_base_store_container(
        container=container,
        container_name=container_name,
        polyaxon_init=polyaxon_init,
        store=artifacts_store,
        command=["polyaxon", "initializer", "tensorboard"],
        args=args,
        env=env,
        env_from=[],
        volume_mounts=volume_mounts,
    )
