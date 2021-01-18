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

from typing import List, Optional

from polyaxon.auxiliaries import V1PolyaxonInitContainer
from polyaxon.constants import DEFAULT
from polyaxon.containers.contexts import (
    CONTEXT_MOUNT_ARTIFACTS,
    CONTEXT_MOUNT_ARTIFACTS_FORMAT,
)
from polyaxon.containers.names import (
    INIT_ARTIFACTS_CONTAINER_PREFIX,
    generate_container_name,
)
from polyaxon.exceptions import PolypodException
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common.mounts import get_artifacts_context_mount
from polyaxon.polypod.init.store import get_base_store_container, get_volume_args
from polyaxon.schemas.types import V1ArtifactsType, V1ConnectionType


def get_artifacts_store_args(artifacts_path: str, clean: bool) -> str:
    get_or_create = 'if [ ! -d "{dir}" ]; then mkdir -m 0777 -p {dir}; fi;'.format(
        dir=artifacts_path
    )
    delete_dir = (
        'if [ -d {path} ] && [ "$(ls -A {path})" ]; '
        "then rm -R {path}/*; fi;".format(path=artifacts_path)
    )
    if clean:
        return "{} {}".format(get_or_create, delete_dir)
    return "{}".format(get_or_create)


def init_artifact_context_args(run_path: str) -> List[str]:
    return [
        'if [ ! -d "{dir}" ]; then mkdir -m 0777 -p {dir}; fi;'.format(
            dir=CONTEXT_MOUNT_ARTIFACTS_FORMAT.format(run_path)
        ),
        'if [ ! -d "{dir}" ]; then mkdir -m 0777 -p {dir}; fi;'.format(
            dir=CONTEXT_MOUNT_ARTIFACTS_FORMAT.format(run_path) + "/outputs"
        ),
    ]


def get_artifacts_path_container(
    polyaxon_init: V1PolyaxonInitContainer,
    artifacts_store: V1ConnectionType,
    run_path: str,
    auto_resume: bool,
) -> Optional[k8s_schemas.V1Container]:
    if not artifacts_store:
        raise PolypodException("Init artifacts container requires a store.")

    init_args = init_artifact_context_args(run_path=run_path)
    if auto_resume:
        init_args.append(
            get_volume_args(
                store=artifacts_store,
                mount_path=CONTEXT_MOUNT_ARTIFACTS,
                artifacts=V1ArtifactsType(dirs=[run_path]),
            )
        )

    container_name = generate_container_name(
        INIT_ARTIFACTS_CONTAINER_PREFIX, DEFAULT, False
    )
    container = k8s_schemas.V1Container(name=container_name)

    return get_base_store_container(
        container_name=container_name,
        container=container,
        polyaxon_init=polyaxon_init,
        store=artifacts_store,
        env=[],
        env_from=[],
        volume_mounts=[get_artifacts_context_mount()],
        # If we are dealing with a volume we need to make sure the path exists for the user
        # We also clean the path if this is not a resume run
        args=[" ".join(init_args)],
    )
