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

from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType


def get_requested_secrets(
    secrets: Iterable[V1K8sResourceType], connections: Iterable[V1ConnectionType]
) -> List[V1K8sResourceType]:
    secrets = secrets or []
    connections = connections or []
    # Create a set of all secrets:
    #   * secrets request by non managed stores
    #   * secrets requested directly by the user
    requested_secrets = [secret for secret in secrets if secret.is_requested]
    secret_ids = {s.name for s in requested_secrets}
    for connection in connections:
        secret = connection.get_secret()
        if secret and secret.name not in secret_ids:
            secret_ids.add(secret.name)
            requested_secrets.append(secret)

    return requested_secrets


def get_requested_config_maps(
    config_maps: Iterable[V1K8sResourceType], connections: Iterable[V1ConnectionType]
) -> List[V1K8sResourceType]:
    config_maps = config_maps or []
    connections = connections or []
    # Create a set of all config_maps:
    #   * secrets request by non managed stores
    #   * secrets requested directly by the user
    requested_config_maps = [
        config_map for config_map in config_maps if config_map.is_requested
    ]
    config_map_ids = {s.name for s in requested_config_maps}
    for connection in connections:
        config_map = connection.get_config_map()
        if config_map and config_map.name not in config_map_ids:
            config_map_ids.add(config_map.name)
            requested_config_maps.append(config_map)

    return requested_config_maps
