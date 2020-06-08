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
import functools
import os

from typing import List, Optional, Tuple

import aiofiles

from polyaxon.polyboard.logging import V1Log, V1Logs
from polyaxon.stores.manager import list_files
from polyaxon.streams.tasks.logs import download_logs_file


@functools.lru_cache(maxsize=30)
def get_logs_files(run_uuid: str) -> List[str]:
    files = list_files(subpath="{}/plxlogs".format(run_uuid))
    if not files["files"]:
        return []
    return sorted([f for f in files["files"].keys()])


async def get_next_file(run_uuid: str, last_file: str = None) -> Optional[str]:
    files = get_logs_files(run_uuid)
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


async def get_archived_operation_logs(
    run_uuid: str, last_file: Optional[str], check_cache: bool = True
) -> Tuple[List[V1Log], Optional[str]]:

    logs = []
    last_file = await get_next_file(run_uuid=run_uuid, last_file=last_file)
    if not last_file:
        return logs, last_file

    logs_path = await download_logs_file(
        run_uuid=run_uuid, last_file=last_file, check_cache=check_cache
    )

    if not os.path.exists(logs_path):
        return logs, last_file

    async with aiofiles.open(logs_path, mode="r") as f:
        contents = await f.read()
        if contents:
            logs = V1Logs.read(contents)
            logs = logs.logs
    return logs, last_file
