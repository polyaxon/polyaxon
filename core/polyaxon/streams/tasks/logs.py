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
from datetime import datetime
from typing import List

import ujson

from starlette import status
from starlette.concurrency import run_in_threadpool
from starlette.exceptions import HTTPException

from polyaxon import settings
from polyaxon.fs.async_manager import (
    delete_file_or_dir,
    download_dir,
    open_file,
    upload_data,
)
from polyaxon.fs.types import FSSystem
from polyaxon.polyboard.logging import V1Log, V1Logs
from polyaxon.utils.path_utils import delete_path


async def clean_tmp_logs(fs: FSSystem, run_uuid: str):
    if not settings.AGENT_CONFIG.artifacts_store:
        raise HTTPException(
            detail="Run's logs was not collected, resource was not found.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    subpath = "{}/.tmpplxlogs".format(run_uuid)
    delete_path(subpath)
    await delete_file_or_dir(fs=fs, subpath=subpath, is_file=False)


async def upload_logs(fs: FSSystem, run_uuid: str, logs: List[V1Log]):
    if not settings.AGENT_CONFIG.artifacts_store:
        raise HTTPException(
            detail="Run's logs was not collected, resource was not found.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    for c_logs in V1Logs.chunk_logs(logs):
        last_file = datetime.timestamp(c_logs.logs[-1].timestamp)
        if settings.AGENT_CONFIG.compressed_logs:
            subpath = "{}/plxlogs/{}.plx".format(run_uuid, last_file)
            await upload_data(
                fs=fs,
                subpath=subpath,
                data="{}\n{}".format(c_logs.get_csv_header(), c_logs.to_csv()),
            )
        else:
            subpath = "{}/plxlogs/{}".format(run_uuid, last_file)
            await upload_data(fs=fs, subpath=subpath, data=c_logs.to_dict(dump=True))


async def content_to_logs(content, logs_path):
    if not content:
        return []

    def convert():
        # Version handling
        if ".plx" in logs_path:
            return V1Logs.read_csv(content).logs
        # Legacy logs
        return ujson.loads(content).get("logs", [])

    return await run_in_threadpool(convert)


async def download_logs_file(
    fs: FSSystem, run_uuid: str, last_file: str, check_cache: bool = True
) -> (str, str):
    subpath = "{}/plxlogs/{}".format(run_uuid, last_file)
    content = await open_file(fs=fs, subpath=subpath, check_cache=check_cache)

    return await content_to_logs(content, subpath)


async def download_tmp_logs(fs: FSSystem, run_uuid: str) -> str:
    subpath = "{}/.tmpplxlogs".format(run_uuid)
    delete_path(subpath)
    return await download_dir(fs=fs, subpath=subpath)
