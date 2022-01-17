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

from typing import List

from polyaxon.auxiliaries import V1PolyaxonInitContainer
from polyaxon.containers.names import INIT_AUTH_CONTAINER
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common.mounts import get_auth_context_mount
from polyaxon.utils.list_utils import to_list


def get_auth_context_container(
    polyaxon_init: V1PolyaxonInitContainer, env: List[k8s_schemas.V1EnvVar] = None
) -> k8s_schemas.V1Container:
    env = to_list(env, check_none=True)
    return k8s_schemas.V1Container(
        name=INIT_AUTH_CONTAINER,
        image=polyaxon_init.get_image(),
        image_pull_policy=polyaxon_init.image_pull_policy,
        command=["polyaxon", "initializer", "auth"],
        env=env,
        resources=polyaxon_init.get_resources(),
        volume_mounts=[get_auth_context_mount(read_only=False)],
    )
