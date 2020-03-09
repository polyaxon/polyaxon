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

import random

from typing import List, Optional

from polyaxon.containers.containers import V1PolyaxonInitContainer
from polyaxon.containers.contexts import (
    CONTEXT_MOUNT_ARTIFACTS,
    CONTEXT_MOUNT_ARTIFACTS_FORMAT,
)
from polyaxon.containers.names import INIT_DOCKERFILE_CONTAINER
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common import constants
from polyaxon.polypod.common.env_vars import get_run_instance_env_var
from polyaxon.polypod.common.mounts import (
    get_auth_context_mount,
    get_connections_context_mount,
)
from polyaxon.polypod.common.volumes import get_volume_name
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1DockerfileType
from polyaxon.utils.list_utils import to_list


def get_dockerfile_init_container(
    polyaxon_init: V1PolyaxonInitContainer,
    dockerfile_args: V1DockerfileType,
    contexts: PluginsContextsSpec,
    run_path: str,
    env: List[k8s_schemas.V1EnvVar] = None,
    mount_path: Optional[str] = None,
) -> k8s_schemas.V1Container:
    env = to_list(env, check_none=True)
    env = env + [get_run_instance_env_var()]

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

    return k8s_schemas.V1Container(
        name=INIT_DOCKERFILE_CONTAINER.format(random.randint(1, 100)),
        image=polyaxon_init.get_image(),
        image_pull_policy=polyaxon_init.image_pull_policy,
        command=["polyaxon", "docker", "generate"],
        args=[
            "--build-context={}".format(dockerfile_args.to_dict(dump=True)),
            "--destination={}".format(mount_path),
            "--copy-path={}".format(
                CONTEXT_MOUNT_ARTIFACTS_FORMAT.format(run_path) + "/outputs"
            ),
        ],
        env=env,
        resources=polyaxon_init.get_resources(),
        volume_mounts=volume_mounts,
    )
