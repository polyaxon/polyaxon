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

from polyaxon.auxiliaries import V1PolyaxonSidecarContainer
from polyaxon.exceptions import PolypodException
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common.env_vars import (
    get_connection_env_var,
    get_env_from_config_map,
    get_env_from_secret,
    get_items_from_config_map,
    get_items_from_secret,
)
from polyaxon.polypod.common.mounts import (
    get_mount_from_resource,
    get_mount_from_store,
    get_mounts,
)
from polyaxon.polypod.sidecar.env_vars import get_sidecar_env_vars
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1ConnectionType
from polyaxon.utils.list_utils import to_list

SIDECAR_CONTAINER = "polyaxon-sidecar"


def get_sidecar_args(
    container_id: str, sleep_interval: int, sync_interval: int, monitor_logs: bool
) -> List[str]:
    args = [
        "--container-id={}".format(container_id),
        "--sleep-interval={}".format(sleep_interval),
        "--sync-interval={}".format(sync_interval),
    ]
    if monitor_logs:
        args.append("--monitor-logs")
    return args


def get_sidecar_container(
    container_id: str,
    polyaxon_sidecar: V1PolyaxonSidecarContainer,
    env: List[k8s_schemas.V1EnvVar],
    artifacts_store: V1ConnectionType,
    contexts: PluginsContextsSpec,
    run_path: Optional[str],
) -> Optional[k8s_schemas.V1Container]:

    if artifacts_store and not contexts:
        raise PolypodException(
            "Logs/artifacts store was passed and contexts was not passed."
        )

    has_artifacts = artifacts_store and contexts.collect_artifacts
    has_logs = artifacts_store and contexts.collect_logs

    if not has_logs and not has_artifacts:
        # No sidecar
        return None

    if (has_artifacts or has_logs) and not run_path:
        raise PolypodException("Logs store/outputs store must have a run_path.")

    env = get_sidecar_env_vars(
        env_vars=env,
        container_id=container_id,
        artifacts_store_name=artifacts_store.name,
    )

    volume_mounts = get_mounts(
        use_auth_context=contexts.auth,
        use_artifacts_context=has_artifacts,
        use_docker_context=False,
        use_shm_context=False,
    )

    sidecar_args = get_sidecar_args(
        container_id=container_id,
        sleep_interval=polyaxon_sidecar.sleep_interval,
        sync_interval=polyaxon_sidecar.sync_interval,
        monitor_logs=polyaxon_sidecar.monitor_logs,
    )

    env_from = []

    secret = None
    if artifacts_store.is_bucket:
        secret = artifacts_store.get_secret()
        volume_mounts += to_list(
            get_mount_from_resource(resource=secret), check_none=True
        )
        env += to_list(get_items_from_secret(secret=secret), check_none=True)
        env_from += to_list(get_env_from_secret(secret=secret), check_none=True)

        config_map = artifacts_store.get_config_map()
        volume_mounts += to_list(
            get_mount_from_resource(resource=config_map), check_none=True
        )
        env += to_list(
            get_items_from_config_map(config_map=config_map), check_none=True
        )
        env_from += to_list(
            get_env_from_config_map(config_map=config_map), check_none=True
        )
    else:
        volume_mounts += to_list(
            get_mount_from_store(store=artifacts_store), check_none=True
        )
    env += to_list(
        get_connection_env_var(connection=artifacts_store, secret=secret),
        check_none=True,
    )

    return k8s_schemas.V1Container(
        name=SIDECAR_CONTAINER,
        image=polyaxon_sidecar.get_image(),
        image_pull_policy=polyaxon_sidecar.image_pull_policy,
        command=["polyaxon", "sidecar"],
        args=sidecar_args,
        env=env,
        env_from=env_from,
        resources=polyaxon_sidecar.get_resources(),
        volume_mounts=volume_mounts,
    )
