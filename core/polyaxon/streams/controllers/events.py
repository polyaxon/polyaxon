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

from typing import Dict, List, Optional, Set

import aiofiles

from starlette import status
from starlette.concurrency import run_in_threadpool
from starlette.exceptions import HTTPException

from polyaxon.fs.async_manager import download_file, list_files
from polyaxon.fs.types import FSSystem
from polyaxon.logger import logger
from polyaxon.polyboard.artifacts import V1ArtifactKind
from polyaxon.polyboard.events import V1Events, get_event_path, get_resource_path


async def get_events_files(fs: FSSystem, run_uuid: str, event_kind: str) -> List[str]:
    subpath = get_event_path(run_path=run_uuid, kind=event_kind)
    files = await list_files(fs=fs, subpath=subpath)
    if not files["files"]:
        return []
    return sorted([f for f in files["files"].keys()])


async def get_resources_files(fs: FSSystem, run_uuid: str) -> List[str]:
    subpath = get_resource_path(run_path=run_uuid, kind=V1ArtifactKind.METRIC)
    files = await list_files(fs=fs, subpath=subpath)
    if not files["files"]:
        return []
    return sorted([f for f in files["files"].keys()])


async def process_operation_event(
    events_path: str,
    event_kind: str,
    event_name: str,
    orient: str = V1Events.ORIENT_CSV,
    sample: int = None,
) -> Optional[Dict]:
    if not events_path or not os.path.exists(events_path):
        return None

    async with aiofiles.open(events_path, mode="r") as f:
        contents = await f.read()
        if contents:
            if orient == V1Events.ORIENT_CSV:
                return {"name": event_name, "kind": event_kind, "data": contents}
            if orient == V1Events.ORIENT_DICT:
                event_df = await run_in_threadpool(
                    V1Events.read,
                    kind=event_kind,
                    name=event_name,
                    data=contents,
                    parse_dates=False,
                )
                if sample:
                    try:
                        sample = int(sample)
                        if event_df.df.shape[0] > sample:
                            event_df.df = event_df.df.sample(n=sample)
                    except Exception as e:
                        logger.warning("Could not sample event dataframe, error %s", e)
                return {
                    "name": event_name,
                    "kind": event_kind,
                    "data": event_df.to_dict(),
                }
            else:
                raise HTTPException(
                    detail="received an unrecognisable orient value {}.".format(orient),
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
    return None


async def get_archived_operation_resource(
    fs: FSSystem,
    run_uuid: str,
    event_kind: str,
    event_name: str,
    orient: str = V1Events.ORIENT_CSV,
    check_cache: bool = True,
    sample: int = None,
) -> Optional[Dict]:

    subpath = get_resource_path(run_path=run_uuid, kind=event_kind, name=event_name)
    events_path = await download_file(fs=fs, subpath=subpath, check_cache=check_cache)

    return await process_operation_event(
        events_path=events_path,
        event_kind=event_kind,
        event_name=event_name,
        orient=orient,
        sample=sample,
    )


async def get_archived_operation_event(
    fs: FSSystem,
    run_uuid: str,
    event_kind: str,
    event_name: str,
    orient: str = V1Events.ORIENT_CSV,
    check_cache: bool = True,
    sample: int = None,
) -> Optional[Dict]:

    subpath = get_event_path(run_path=run_uuid, kind=event_kind, name=event_name)
    events_path = await download_file(fs=fs, subpath=subpath, check_cache=check_cache)

    return await process_operation_event(
        events_path=events_path,
        event_kind=event_kind,
        event_name=event_name,
        orient=orient,
        sample=sample,
    )


async def get_archived_operation_resources(
    fs: FSSystem,
    run_uuid: str,
    event_kind: str,
    event_names: Set[str],
    orient: str = V1Events.ORIENT_CSV,
    check_cache: bool = True,
    sample: int = None,
) -> List[Dict]:
    events = []
    if not event_names:
        files = await get_resources_files(fs=fs, run_uuid=run_uuid)
        event_names = [f.split(".plx")[0] for f in files]
    for event_name in event_names:
        event = await get_archived_operation_resource(
            fs=fs,
            run_uuid=run_uuid,
            event_kind=event_kind,
            event_name=event_name,
            orient=orient,
            check_cache=check_cache,
            sample=sample,
        )
        if event:
            events.append(event)
    return events


async def get_archived_operation_events(
    fs: FSSystem,
    run_uuid: str,
    event_kind: str,
    event_names: Set[str],
    orient: str = V1Events.ORIENT_CSV,
    check_cache: bool = True,
    sample: int = None,
) -> List[Dict]:
    events = []
    for event_name in event_names:
        event = await get_archived_operation_event(
            fs=fs,
            run_uuid=run_uuid,
            event_kind=event_kind,
            event_name=event_name,
            orient=orient,
            check_cache=check_cache,
            sample=sample,
        )
        if event:
            events.append(event)
    return events


async def get_archived_operations_events(
    fs: FSSystem,
    event_kind: str,
    run_uuids: Set[str],
    event_names: Set[str],
    orient: str = V1Events.ORIENT_CSV,
    check_cache: bool = True,
    sample: int = None,
) -> Dict[str, List]:
    events = {}
    for run_uuid in run_uuids:
        run_events = await get_archived_operation_events(
            fs=fs,
            run_uuid=run_uuid,
            event_kind=event_kind,
            event_names=event_names,
            orient=orient,
            check_cache=check_cache,
            sample=sample,
        )
        events[run_uuid] = run_events
    return events
