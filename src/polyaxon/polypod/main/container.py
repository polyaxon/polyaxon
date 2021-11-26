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

from typing import Dict, Iterable, List, Optional

from polyaxon.exceptions import PolypodException
from polyaxon.k8s import k8s_schemas
from polyaxon.polyflow import V1Init
from polyaxon.polypod.common.containers import patch_container
from polyaxon.polypod.common.env_vars import get_env_from_k8s_resources
from polyaxon.polypod.main.env_vars import get_env_vars
from polyaxon.polypod.main.k8s_resources import (
    get_requested_config_maps,
    get_requested_secrets,
)
from polyaxon.polypod.main.volumes import get_volume_mounts
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType
from polyaxon.utils.list_utils import to_list


def get_main_container(
    container_id: str,
    main_container: k8s_schemas.V1Container,
    volume_mounts: List[k8s_schemas.V1VolumeMount],
    contexts: PluginsContextsSpec,
    artifacts_store: Optional[V1ConnectionType],
    init: Optional[List[V1Init]],
    connections: Optional[List[str]],
    connection_by_names: Dict[str, V1ConnectionType],
    secrets: Optional[Iterable[V1K8sResourceType]],
    config_maps: Optional[Iterable[V1K8sResourceType]],
    log_level: str,
    run_path: Optional[str],
    kv_env_vars: List[List] = None,
    env: List[k8s_schemas.V1EnvVar] = None,
    ports: List[int] = None,
) -> k8s_schemas.V1Container:
    """Pod job container for task."""
    connections = connections or []
    connection_by_names = connection_by_names or {}
    secrets = secrets or []
    config_maps = config_maps or []

    if artifacts_store and not run_path:
        raise PolypodException("Run path is required for main container.")

    if artifacts_store and (
        not contexts.collect_artifacts or contexts.mount_artifacts_store
    ):
        if artifacts_store.name not in connection_by_names:
            connection_by_names[artifacts_store.name] = artifacts_store
        if artifacts_store.name not in connections:
            connections.append(artifacts_store.name)

    requested_connections = [connection_by_names[c] for c in connections]
    requested_config_maps = get_requested_config_maps(
        config_maps=config_maps, connections=requested_connections
    )
    requested_secrets = get_requested_secrets(
        secrets=secrets, connections=requested_connections
    )

    # Mounts
    volume_mounts = to_list(volume_mounts, check_none=True)
    volume_mounts = volume_mounts + get_volume_mounts(
        contexts=contexts,
        init=init,
        connections=requested_connections,
        secrets=requested_secrets,
        config_maps=requested_config_maps,
    )

    # Env vars
    env = to_list(env, check_none=True)
    env = env + get_env_vars(
        contexts=contexts,
        log_level=log_level,
        kv_env_vars=kv_env_vars,
        artifacts_store_name=artifacts_store.name if artifacts_store else None,
        connections=requested_connections,
        secrets=requested_secrets,
        config_maps=requested_config_maps,
    )

    # Env from
    env_from = get_env_from_k8s_resources(
        secrets=requested_secrets, config_maps=requested_config_maps
    )

    ports = [
        k8s_schemas.V1ContainerPort(container_port=port)
        for port in to_list(ports, check_none=True)
    ]

    return patch_container(
        container=main_container,
        name=container_id,
        env=env,
        env_from=env_from,
        volume_mounts=volume_mounts,
        ports=ports or None,
    )
