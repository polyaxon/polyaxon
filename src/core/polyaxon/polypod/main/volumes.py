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

from typing import Iterable, List, Optional

from polyaxon.containers.contexts import CONTEXT_MOUNT_ARTIFACTS
from polyaxon.k8s import k8s_schemas
from polyaxon.polyflow import V1Init
from polyaxon.polypod.common import constants
from polyaxon.polypod.common.mounts import (
    get_artifacts_context_mount,
    get_connections_context_mount,
    get_mount_from_resource,
    get_mount_from_store,
)
from polyaxon.polypod.common.volumes import get_volume_name
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType
from polyaxon.utils.list_utils import to_list


def get_volume_mounts(
    contexts: PluginsContextsSpec,
    init: Optional[List[V1Init]],
    connections: Iterable[V1ConnectionType],
    secrets: Iterable[V1K8sResourceType],
    config_maps: Iterable[V1K8sResourceType] = None,
) -> List[k8s_schemas.V1VolumeMount]:
    init = init or []
    connections = connections or []
    secrets = secrets or []
    config_maps = config_maps or []

    volume_mounts = []
    volume_names = set()
    if contexts and contexts.collect_artifacts:
        volume_mounts += to_list(
            get_artifacts_context_mount(read_only=False), check_none=True
        )
        volume_names.add(constants.CONTEXT_VOLUME_ARTIFACTS)
    for init_connection in init:
        volume_name = (
            get_volume_name(init_connection.path)
            if init_connection.path
            else constants.CONTEXT_VOLUME_ARTIFACTS
        )
        mount_path = init_connection.path or CONTEXT_MOUNT_ARTIFACTS
        if volume_name in volume_names:
            continue
        volume_names.add(volume_name)
        volume_mounts += to_list(
            get_connections_context_mount(name=volume_name, mount_path=mount_path),
            check_none=True,
        )
    for store in connections:
        volume_mounts += to_list(get_mount_from_store(store=store), check_none=True)

    for secret in secrets:
        volume_mounts += to_list(
            get_mount_from_resource(resource=secret), check_none=True
        )

    for config_map in config_maps:
        volume_mounts += to_list(
            get_mount_from_resource(resource=config_map), check_none=True
        )

    return volume_mounts
