#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from polyaxon.contexts import paths as ctx_paths
from polyaxon.fs.watcher import FSWatcher
from polyaxon.logger import logger
from polyaxon.schemas.types import V1ConnectionType
from polyaxon.utils.formatting import Printer


def sync_file_watcher(path: str):
    try:
        fw = FSWatcher()
        fw.sync(path)
        fw.write(ctx_paths.CONTEXT_MOUNT_FILE_WATCHER)
    except Exception as e:  # File watcher should not prevent job from starting
        logger.warning(
            "File watcher failed syncing path: {}.\nError: {}".format(path, e)
        )


def download_artifact(
    connection_name: str,
    connection_kind: str,
    path_from: str,
    path_to: str,
    is_file: bool,
    raise_errors: bool,
    sync_fw: bool,
    check_path: bool,
):
    from polyaxon.fs.fs import get_sync_fs_from_type
    from polyaxon.fs.manager import download_file_or_dir

    connection_type = V1ConnectionType(name=connection_name, kind=connection_kind)
    fs = get_sync_fs_from_type(connection_type=connection_type)

    try:
        download_file_or_dir(
            fs=fs,
            path_from=path_from,
            path_to=path_to,
            is_file=is_file,
            check_path=check_path,
        )
        if sync_fw:
            sync_file_watcher(path_to)
        Printer.print_success(
            "{} path is initialized, path: `{}`".format(connection_kind, path_to)
        )
    except Exception as e:
        if raise_errors:
            raise e
        else:
            logger.debug(
                "Initialization failed, the error was ignored. Error details %s", e
            )
