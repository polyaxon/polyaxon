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

import os

from typing import Optional

import aiofiles

from polyaxon import settings
from polyaxon.exceptions import PolyaxonException
from polyaxon.logger import logger
from polyaxon.stores import manager
from polyaxon.utils.path_utils import check_or_create_path, get_path


async def upload_data(subpath: str, data):
    path_to = get_path(settings.AGENT_CONFIG.artifacts_store.store_path, subpath)
    path_from = os.path.join(settings.AGENT_CONFIG.artifacts_root, subpath)
    check_or_create_path(path_from, is_dir=False)
    async with aiofiles.open(path_from, "w") as filepath_upload:
        await filepath_upload.write(data)
    manager.upload_file_or_dir(
        connection_type=settings.AGENT_CONFIG.artifacts_store,
        path_from=path_from,
        path_to=path_to,
        is_file=True,
    )


async def download_file(subpath: str, check_cache=True) -> Optional[str]:
    path_from = get_path(settings.AGENT_CONFIG.artifacts_store.store_path, subpath)
    path_to = os.path.join(settings.CLIENT_CONFIG.archive_root, subpath)

    if os.path.exists(path_to):
        if check_cache:
            # file already exists
            return path_to
        else:
            os.remove(path_to)

    check_or_create_path(path_to, is_dir=False)
    try:
        return manager.download_file_or_dir(
            connection_type=settings.AGENT_CONFIG.artifacts_store,
            path_from=path_from,
            path_to=path_to,
            is_file=True,
        )
    except (OSError, PolyaxonException) as e:
        logger.warning("Could not download %s. Error %s" % (path_from, e))
        return None


async def download_dir(subpath: str, to_tar: bool = False) -> Optional[str]:
    path_from = get_path(settings.AGENT_CONFIG.artifacts_store.store_path, subpath)
    path_to = os.path.join(settings.CLIENT_CONFIG.archive_root, subpath)
    check_or_create_path(path_to, is_dir=True)
    try:
        return manager.download_file_or_dir(
            connection_type=settings.AGENT_CONFIG.artifacts_store,
            path_from=path_from,
            path_to=path_to,
            is_file=False,
            workers=5,
            to_tar=to_tar,
        )
    except (OSError, PolyaxonException) as e:
        logger.warning("Could not download %s. Error %s" % (path_from, e))
        return None


async def list_files(subpath: str, filepath) -> str:
    return manager.list_files(
        connection_type=settings.AGENT_CONFIG.artifacts_store,
        subpath=subpath,
        filepath=filepath,
    )


async def delete_file(subpath: str) -> bool:
    try:
        manager.delete_file_or_dir(
            connection_type=settings.AGENT_CONFIG.artifacts_store,
            subpath=subpath,
            is_file=True,
        )
        return True
    except (OSError, PolyaxonException) as e:
        logger.warning("Could not delete %s. Error %s" % (subpath, e))
        return False


async def delete_dir(subpath: str) -> bool:
    try:
        manager.delete_file_or_dir(
            connection_type=settings.AGENT_CONFIG.artifacts_store,
            subpath=subpath,
            is_file=False,
            workers=5,
        )
        return True
    except (OSError, PolyaxonException) as e:
        logger.warning("Could not delete %s. Error %s" % (subpath, e))
        return False
