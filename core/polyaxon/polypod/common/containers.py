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
import json

from collections.abc import Mapping
from typing import Dict, List

from polyaxon.containers.names import generate_container_name
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common.container_resources import sanitize_resources
from polyaxon.utils.list_utils import to_list


def patch_container(
    container: k8s_schemas.V1Container,
    name: str = None,
    command: List[str] = None,
    args: List[str] = None,
    image: str = None,
    image_pull_policy: str = None,
    env: List[k8s_schemas.V1EnvVar] = None,
    env_from: List[k8s_schemas.V1EnvFromSource] = None,
    volume_mounts: List[k8s_schemas.V1VolumeMount] = None,
    ports: List[k8s_schemas.V1ContainerPort] = None,
    resources: k8s_schemas.V1ResourceRequirements = None,
) -> k8s_schemas.V1Container:
    container.name = sanitize_container_name(name or container.name)
    container.env = to_list(container.env, check_none=True) + to_list(
        env, check_none=True
    )
    container.env_from = to_list(container.env_from, check_none=True) + to_list(
        env_from, check_none=True
    )
    container.volume_mounts = to_list(
        container.volume_mounts, check_none=True
    ) + to_list(volume_mounts, check_none=True)
    container.ports = to_list(container.ports, check_none=True) + to_list(
        ports, check_none=True
    )
    container.resources = container.resources or resources
    container.image_pull_policy = container.image_pull_policy or image_pull_policy
    container.image = container.image or image

    if not any([container.command, container.args]):
        container.command = command
        container.args = args

    return sanitize_container(container)


def sanitize_container_name(name: str) -> str:
    name = name.replace("_", "-")
    return name.lower()


def ensure_container_name(
    container: k8s_schemas.V1Container, prefix: str = None
) -> k8s_schemas.V1Container:
    if not container:
        return container

    name = container.name
    if not name:
        container.name = generate_container_name(prefix=prefix)
    return container


def sanitize_container_command_args(
    container: k8s_schemas.V1Container,
) -> k8s_schemas.V1Container:
    # Sanitize container command/args
    if container.command:
        container.command = [
            str(c) for c in to_list(container.command, check_none=True) if c
        ]
    if container.args:
        container.args = [str(c) for c in to_list(container.args, check_none=True) if c]

    return container


def sanitize_container_env(
    container: k8s_schemas.V1Container,
) -> k8s_schemas.V1Container:
    def sanitize_env_dict(d: Dict):
        return {
            d_k: sanitize_value(d_v, handle_dict=False)
            if d_k in ["name", "value"]
            else sanitize_value(d_v, handle_dict=True)
            for d_k, d_v in d.items()
        }

    def sanitize_value(d, handle_dict: bool = False):
        if isinstance(d, str):
            return d
        if not isinstance(d, Mapping):
            return json.dumps(d)
        if not handle_dict:
            return json.dumps(d)
        return {d_k: sanitize_value(d_v, handle_dict=True) for d_k, d_v in d.items()}

    if container.env:
        env = []
        for e in container.env:
            if isinstance(e, Mapping):
                e = sanitize_env_dict(e)
                env.append(e)
            elif isinstance(e, k8s_schemas.V1EnvVar):
                if e.value is not None:
                    e.value = sanitize_value(e.value, handle_dict=False)
                env.append(e)

        container.env = env
    return container


def sanitize_container(
    container: k8s_schemas.V1Container,
) -> k8s_schemas.V1Container:
    container = sanitize_container_command_args(container)
    container.resources = sanitize_resources(container.resources)
    return sanitize_container_env(container)
