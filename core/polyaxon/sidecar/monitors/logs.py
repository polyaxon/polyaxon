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

from typing import Optional

import aiofiles

from kubernetes_asyncio.client.models import V1Pod

from polyaxon.containers.contexts import CONTEXT_MOUNT_ARTIFACTS_FORMAT
from polyaxon.k8s.async_manager import AsyncK8SManager
from polyaxon.k8s.logging.async_monitor import query_k8s_pod_logs
from polyaxon.polyboard.logging import V1Logs
from polyaxon.types import AwareDT
from polyaxon.utils.path_utils import check_or_create_path, delete_path


async def sync_logs(
    run_uuid: str,
    k8s_manager: AsyncK8SManager,
    pod: V1Pod,
    last_time: Optional[AwareDT],
    stream: bool = False,
    is_running: bool = True,
):
    path_from = CONTEXT_MOUNT_ARTIFACTS_FORMAT.format(run_uuid)
    path_from = "{}/.tmpplxlogs".format(path_from)

    if not is_running:
        delete_path(path_from)
        return

    logs, _ = await query_k8s_pod_logs(
        k8s_manager=k8s_manager,
        pod=pod,
        last_time=last_time,
        stream=stream,
    )
    if not logs:
        return

    path_from = "{}/{}.plx".format(path_from, pod.metadata.name)
    check_or_create_path(path_from, is_dir=False)
    async with aiofiles.open(path_from, "w") as filepath:
        _logs = V1Logs(logs=logs)
        await filepath.write("{}\n{}".format(_logs.get_csv_header(), _logs.to_csv()))
