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

from polyaxon.containers.contexts import (
    CONTEXT_MOUNT_ARTIFACTS,
    CONTEXT_MOUNT_ARTIFACTS_FORMAT,
    CONTEXT_MOUNT_ARTIFACTS_RELATED,
    CONTEXT_MOUNT_ARTIFACTS_RELATED_FORMAT,
)
from polyaxon.fs.async_manager import sync_fs
from polyaxon.fs.types import FSSystem
from polyaxon.fs.watcher import FSWatcher

IGNORE_FOLDERS = ["plxlogs", ".git"]


async def sync_artifacts(fs: FSSystem, fw: FSWatcher, store_path: str, run_uuid: str):
    fw.init()
    path_from = CONTEXT_MOUNT_ARTIFACTS_FORMAT.format(run_uuid)
    fw.sync(path_from, exclude=IGNORE_FOLDERS)

    # Check if this run has triggered some related run paths
    if os.path.exists(CONTEXT_MOUNT_ARTIFACTS_RELATED):
        for sub_path in os.listdir(CONTEXT_MOUNT_ARTIFACTS_RELATED):
            # check if there's a path to sync
            path_from = CONTEXT_MOUNT_ARTIFACTS_RELATED_FORMAT.format(sub_path)
            fw.sync(path_from, exclude=IGNORE_FOLDERS)

    await sync_fs(
        fs=fs,
        fw=fw,
        store_base_path=store_path,
        context_base_path=CONTEXT_MOUNT_ARTIFACTS,
    )
