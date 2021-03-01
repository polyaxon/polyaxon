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

from starlette import status
from starlette.exceptions import HTTPException

from polyaxon import settings
from polyaxon.polyboard.logging import V1Log, V1Logs
from polyaxon.stores.async_manager import (
    delete_dir,
    download_dir,
    download_file,
    upload_data,
)
from polyaxon.utils.path_utils import delete_path


async def clean_tmp_logs(run_uuid: str):
    if not settings.AGENT_CONFIG.artifacts_store:
        raise HTTPException(
            detail="Run's logs was not collected, resource was not found.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    subpath = "{}/.tmpplxlogs".format(run_uuid)
    delete_path(subpath)
    await delete_dir(subpath=subpath)


async def upload_logs(run_uuid: str, logs: List[V1Log]):
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
                subpath=subpath,
                data="{}\n{}".format(c_logs.get_csv_header(), c_logs.to_csv()),
            )
        else:
            subpath = "{}/plxlogs/{}".format(run_uuid, last_file)
            await upload_data(subpath=subpath, data=c_logs.to_dict(dump=True))


async def download_logs_file(
    run_uuid: str, last_file: str, check_cache: bool = True
) -> str:
    subpath = "{}/plxlogs/{}".format(run_uuid, last_file)
    return await download_file(subpath, check_cache=check_cache)


async def download_tmp_logs(run_uuid: str) -> str:
    subpath = "{}/.tmpplxlogs".format(run_uuid)
    delete_path(subpath)
    return await download_dir(subpath)
