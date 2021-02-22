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

import os

from typing import List, Optional, Tuple

import aiofiles

from polyaxon.k8s.async_manager import AsyncK8SManager
from polyaxon.k8s.logging.async_monitor import query_k8s_operation_logs
from polyaxon.polyboard.logging import V1Log, V1Logs
from polyaxon.stores.manager import list_files
from polyaxon.streams.tasks.logs import download_logs_file, download_tmp_logs
from polyaxon.types import AwareDT


def get_logs_files(run_uuid: str) -> List[str]:
    files = list_files(subpath="{}/plxlogs".format(run_uuid))
    if not files["files"]:
        return []
    return sorted([f for f in files["files"].keys()])


async def get_next_file(files: List[str], last_file: str = None) -> Optional[str]:
    if not files:
        return None

    if not last_file:
        return files[0]

    i = 0
    for i, f in enumerate(files):
        if f == last_file:
            break
    i += 1
    if i >= len(files):
        return None

    return files[i]


async def read_logs_file(logs_path) -> List[V1Log]:
    if not os.path.exists(logs_path):
        return []

    async with aiofiles.open(logs_path, mode="r") as f:
        contents = await f.read()
        if contents:
            # Version handling
            if ".plx" in logs_path:
                return V1Logs.read_csv(contents).logs
            # Legacy logs
            logs = V1Logs.read(contents)
            return logs.logs

    return []


async def get_archived_operation_logs(
    run_uuid: str, last_file: Optional[str], check_cache: bool = True
) -> Tuple[List[V1Log], Optional[str], List[str]]:
    files = get_logs_files(run_uuid)
    logs = []
    last_file = await get_next_file(files=files, last_file=last_file)
    if not last_file:
        return logs, last_file, files

    logs_path = await download_logs_file(
        run_uuid=run_uuid, last_file=last_file, check_cache=check_cache
    )

    logs = await read_logs_file(logs_path)

    return logs, last_file, files


async def get_tmp_operation_logs(
    run_uuid: str, last_time: Optional[AwareDT]
) -> Tuple[List[V1Log], Optional[AwareDT]]:

    logs = []

    tmp_logs = await download_tmp_logs(run_uuid=run_uuid)

    if not os.path.exists(tmp_logs):
        return logs, None

    tmp_log_files = os.listdir(tmp_logs)
    if not tmp_log_files:
        return logs, None

    for tmp_file in tmp_log_files:
        logs_path = os.path.join(tmp_logs, tmp_file)
        logs += await read_logs_file(logs_path)

    if last_time:
        logs = [l for l in logs if l.timestamp > last_time]
    if logs:
        logs = sorted(logs, key=lambda x: x.timestamp)
        last_time = logs[-1].timestamp
    return logs, last_time


async def get_operation_logs(
    k8s_manager: AsyncK8SManager,
    k8s_operation: any,
    instance: str,
    last_time: Optional[AwareDT],
):
    previous_last = last_time
    operation_logs, last_time = await query_k8s_operation_logs(
        instance=instance,
        last_time=None,
        k8s_manager=k8s_manager,
        stream=True,
    )
    if k8s_operation["status"].get("completionTime"):
        last_time = None
    if previous_last:
        operation_logs = [l for l in operation_logs if l.timestamp > previous_last]

    return operation_logs, last_time
