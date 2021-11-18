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
import asyncio
import os

from typing import List

from polyaxon.containers.contexts import (
    CONTEXT_MOUNT_ARTIFACTS_FORMAT,
    CONTEXT_MOUNT_ARTIFACTS_RELATED,
    CONTEXT_MOUNT_ARTIFACTS_RELATED_FORMAT,
)
from polyaxon.fs.async_manager import ensure_async_execution
from polyaxon.fs.types import FSSystem
from polyaxon.fs.watcher import FSWatcher
from polyaxon.logger import logger


async def sync_fs(
    fs: FSSystem,
    fw: FSWatcher,
    store_base_path: str,
):
    def get_store_path(subpath: str):
        return os.path.join(store_base_path, subpath)

    rm_files = fw.get_files_to_rm()
    logger.debug("rm_files {}".format(rm_files))
    await asyncio.gather(
        *[
            ensure_async_execution(
                fs=fs,
                fct="rm_file",
                is_async=fs.async_impl,
                path=get_store_path(subpath),
                recursive=False,
            )
            for (_, subpath) in rm_files
        ],
        return_exceptions=True
    )
    rm_dirs = fw.get_dirs_to_rm()
    logger.debug("rm_dirs {}".format(rm_dirs))
    await asyncio.gather(
        *[
            ensure_async_execution(
                fs=fs,
                fct="rm",
                is_async=fs.async_impl,
                path=get_store_path(subpath),
                recursive=True,
            )
            for (_, subpath) in rm_dirs
        ],
        return_exceptions=True
    )
    put_files = fw.get_files_to_put()
    logger.debug("put_files {}".format(put_files))
    await asyncio.gather(
        *[
            ensure_async_execution(
                fs=fs,
                fct="put",
                is_async=fs.async_impl,
                lpath=os.path.join(r_base_path, subpath),
                rpath=get_store_path(subpath),
                recursive=False,
            )
            for (r_base_path, subpath) in put_files
        ],
        return_exceptions=True
    )


async def sync_artifacts(
    fs: FSSystem,
    fw: FSWatcher,
    store_path: str,
    run_uuid: str,
    exclude: List[str] = None,
):
    fw.init()
    path_from = CONTEXT_MOUNT_ARTIFACTS_FORMAT.format(run_uuid)
    fw.sync(path_from, exclude=exclude)

    # Check if this run has triggered some related run paths
    if os.path.exists(CONTEXT_MOUNT_ARTIFACTS_RELATED):
        for sub_path in os.listdir(CONTEXT_MOUNT_ARTIFACTS_RELATED):
            # check if there's a path to sync
            path_from = CONTEXT_MOUNT_ARTIFACTS_RELATED_FORMAT.format(sub_path)
            fw.sync(path_from, exclude=exclude)

    await sync_fs(
        fs=fs,
        fw=fw,
        store_base_path=store_path,
    )
