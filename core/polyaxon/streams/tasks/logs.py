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
from datetime import datetime
from typing import List

from starlette import status
from starlette.exceptions import HTTPException

from polyaxon import settings
from polyaxon.polyboard.logging import V1Log, V1Logs
from polyaxon.streams.stores.async_manager import download_file, upload_data


async def upload_logs(run_uuid: str, logs: List[V1Log]):
    if not settings.AGENT_CONFIG.artifacts_store:
        raise HTTPException(
            detail="Run's logs was not collected, resource was not found.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    for c_logs in V1Logs.chunk_logs(logs):
        last_file = datetime.timestamp(c_logs.logs[-1].timestamp)
        subpath = "{}/plxlogs/{}".format(run_uuid, last_file)
        await upload_data(subpath=subpath, data=c_logs.to_dict(dump=True))


async def download_logs_file(
    run_uuid: str, last_file: str, check_cache: bool = True
) -> str:
    subpath = "{}/plxlogs/{}".format(run_uuid, last_file)
    return await download_file(subpath, check_cache=check_cache)
