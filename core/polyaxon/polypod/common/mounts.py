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

from polyaxon.containers.contexts import (
    CONTEXT_MOUNT_ARTIFACTS,
    CONTEXT_MOUNT_CONFIGS,
    CONTEXT_MOUNT_DOCKER,
    CONTEXT_MOUNT_SHM,
)
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common import constants
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType


def get_mount_from_store(
    store: V1ConnectionType,
) -> Optional[k8s_schemas.V1VolumeMount]:
    if not store or not store.is_mount:
        return None

    return k8s_schemas.V1VolumeMount(
        name=store.name,
        mount_path=store.schema.mount_path,
        read_only=store.schema.read_only,
    )


def get_mount_from_resource(
    resource: V1K8sResourceType,
) -> Optional[k8s_schemas.V1VolumeMount]:
    if not resource or not resource.schema.mount_path:
        return None

    return k8s_schemas.V1VolumeMount(
        name=resource.name, mount_path=resource.schema.mount_path, read_only=True
    )


def get_docker_context_mount() -> k8s_schemas.V1VolumeMount:
    return k8s_schemas.V1VolumeMount(
        name=constants.CONTEXT_VOLUME_DOCKER, mount_path=CONTEXT_MOUNT_DOCKER
    )


def get_auth_context_mount(read_only=None) -> k8s_schemas.V1VolumeMount:
    return k8s_schemas.V1VolumeMount(
        name=constants.CONTEXT_VOLUME_CONFIGS,
        mount_path=CONTEXT_MOUNT_CONFIGS,
        read_only=read_only,
    )


def get_artifacts_context_mount(read_only=None) -> k8s_schemas.V1VolumeMount:
    return k8s_schemas.V1VolumeMount(
        name=constants.CONTEXT_VOLUME_ARTIFACTS,
        mount_path=CONTEXT_MOUNT_ARTIFACTS,
        read_only=read_only,
    )


def get_connections_context_mount(
    name: str, mount_path: str
) -> k8s_schemas.V1VolumeMount:
    return k8s_schemas.V1VolumeMount(name=name, mount_path=mount_path)


def get_shm_context_mount() -> k8s_schemas.V1VolumeMount:
    """
    Mount an tmpfs volume to /dev/shm.
    This will set /dev/shm size to half of the RAM of node.
    By default, /dev/shm is very small, only 64MB.
    Some experiments will fail due to lack of share memory,
    such as some experiments running on Pytorch.
    """
    return k8s_schemas.V1VolumeMount(
        name=constants.CONTEXT_VOLUME_SHM, mount_path=CONTEXT_MOUNT_SHM
    )


def get_mounts(
    use_auth_context: bool,
    use_docker_context: bool,
    use_shm_context: bool,
    use_artifacts_context: bool,
) -> List[k8s_schemas.V1VolumeMount]:
    mounts = []
    if use_auth_context:
        mounts.append(get_auth_context_mount(read_only=True))
    if use_artifacts_context:
        mounts.append(get_artifacts_context_mount(read_only=False))
    if use_docker_context:
        mounts.append(get_docker_context_mount())
    if use_shm_context:
        mounts.append(get_shm_context_mount())

    return mounts
