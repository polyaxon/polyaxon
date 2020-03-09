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
import uuid

from typing import Optional

from polyaxon.containers.contexts import CONTEXT_MOUNT_DOCKER
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common import constants
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType


def get_volume_name(path: str) -> str:
    name = uuid.uuid5(namespace=uuid.NAMESPACE_DNS, name=path).hex
    return constants.CONTEXT_VOLUME_CONNECTIONS_FORMAT.format(name)


def get_volume_from_connection(
    connection: V1ConnectionType,
) -> Optional[k8s_schemas.V1Volume]:
    if not connection:
        return None
    if connection.is_volume_claim:
        pv_claim = k8s_schemas.V1PersistentVolumeClaimVolumeSource(
            claim_name=connection.schema.volume_claim,
            read_only=connection.schema.read_only,
        )
        return k8s_schemas.V1Volume(
            name=connection.name, persistent_volume_claim=pv_claim
        )

    if connection.is_host_path:
        return k8s_schemas.V1Volume(
            name=connection.name,
            host_path=k8s_schemas.V1HostPathVolumeSource(
                path=connection.schema.host_path
            ),
        )


def get_volume_from_secret(secret: V1K8sResourceType) -> Optional[k8s_schemas.V1Volume]:
    if not secret:
        return None
    if secret.schema.mount_path:
        secret_volume = k8s_schemas.V1SecretVolumeSource(
            secret_name=secret.name, items=secret.schema.items
        )
        return k8s_schemas.V1Volume(name=secret.name, secret=secret_volume)


def get_volume_from_config_map(
    config_map: V1K8sResourceType,
) -> Optional[k8s_schemas.V1Volume]:
    if not config_map:
        return None
    if config_map.schema.mount_path:
        config_map_volume = k8s_schemas.V1ConfigMapVolumeSource(
            name=config_map.name, items=config_map.schema.items
        )
        return k8s_schemas.V1Volume(name=config_map.name, config_map=config_map_volume)


def get_volume(
    volume: str, claim_name: str = None, host_path: str = None, read_only: bool = None
) -> k8s_schemas.V1Volume:
    if claim_name:
        pv_claim = k8s_schemas.V1PersistentVolumeClaimVolumeSource(
            claim_name=claim_name, read_only=read_only
        )
        return k8s_schemas.V1Volume(name=volume, persistent_volume_claim=pv_claim)

    if host_path:
        return k8s_schemas.V1Volume(
            name=volume, host_path=k8s_schemas.V1HostPathVolumeSource(path=host_path)
        )

    empty_dir = k8s_schemas.V1EmptyDirVolumeSource()
    return k8s_schemas.V1Volume(name=volume, empty_dir=empty_dir)


def get_docker_context_volume() -> k8s_schemas.V1Volume:
    return get_volume(
        volume=constants.CONTEXT_VOLUME_DOCKER, host_path=CONTEXT_MOUNT_DOCKER
    )


def get_configs_context_volume() -> k8s_schemas.V1Volume:
    return get_volume(volume=constants.CONTEXT_VOLUME_CONFIGS)


def get_artifacts_context_volume() -> k8s_schemas.V1Volume:
    return get_volume(volume=constants.CONTEXT_VOLUME_ARTIFACTS)


def get_connections_context_volume(name: str) -> k8s_schemas.V1Volume:
    return get_volume(volume=name)


def get_shm_context_volume() -> k8s_schemas.V1Volume:
    """
    Mount an tmpfs volume to /dev/shm.
    This will set /dev/shm size to half of the RAM of node.
    By default, /dev/shm is very small, only 64MB.
    Some experiments will fail due to lack of share memory,
    such as some experiments running on Pytorch.
    """
    return k8s_schemas.V1Volume(
        name=constants.CONTEXT_VOLUME_SHM,
        empty_dir=k8s_schemas.V1EmptyDirVolumeSource(medium="Memory"),
    )
