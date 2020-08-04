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

from datetime import datetime
from typing import List, Optional

from polyaxon import settings
from polyaxon.connections.getter import get_connection_from_type
from polyaxon.connections.reader import get_connection_type
from polyaxon.env_vars.keys import POLYAXON_KEYS_ARTIFACTS_STORE_NAME
from polyaxon.exceptions import PolyaxonStoresException
from polyaxon.schemas.types import V1ConnectionType
from polyaxon.utils.path_utils import create_tarfile, get_files_in_path, get_path


def get_artifacts_store_name():
    """Get the artifacts store name"""
    return os.getenv(POLYAXON_KEYS_ARTIFACTS_STORE_NAME)


def get_artifacts_connection() -> Optional[V1ConnectionType]:
    store_name = get_artifacts_store_name()
    if store_name:
        return get_connection_type(store_name)
    if settings.AGENT_CONFIG:
        return settings.AGENT_CONFIG.artifacts_store
    return None


def validate_store(connection_type: V1ConnectionType):
    if not connection_type or not connection_type.is_artifact:
        raise PolyaxonStoresException("An artifact store type was not provided.")


def list_files(
    subpath: str, filepath: str = None, connection_type: V1ConnectionType = None
):
    connection_type = connection_type or get_artifacts_connection()

    validate_store(connection_type)

    store_path = get_path(connection_type.store_path, subpath)
    if filepath:
        store_path = get_path(store_path, filepath)

    store_manager = get_connection_from_type(connection_type=connection_type)

    try:
        results = store_manager.ls(store_path)
        results["files"] = {f[0]: f[1] for f in results["files"]}
        return results
    except Exception:
        raise PolyaxonStoresException(
            "Run store path does not exists or bad configuration."
        )


def upload_file_or_dir(
    path_from: str,
    path_to: str,
    is_file: bool,
    workers: int = 0,
    last_time: datetime = None,
    connection_type: V1ConnectionType = None,
    exclude: List[str] = None,
):
    connection_type = connection_type or get_artifacts_connection()

    validate_store(connection_type)
    store_manager = get_connection_from_type(connection_type=connection_type)

    if is_file:
        store_manager.upload_file(path_from, path_to, use_basename=False)
    else:
        store_manager.upload_dir(
            path_from,
            path_to,
            use_basename=False,
            workers=workers,
            last_time=last_time,
            exclude=exclude,
        )


def download_file_or_dir(
    path_from: str,
    path_to: str,
    is_file: bool,
    workers: int = 0,
    connection_type: V1ConnectionType = None,
    to_tar: bool = False,
) -> Optional[str]:
    connection_type = connection_type or get_artifacts_connection()

    validate_store(connection_type)
    store_manager = get_connection_from_type(connection_type=connection_type)

    if is_file:
        store_manager.download_file(path_from, path_to, use_basename=False)
    else:
        store_manager.download_dir(
            path_from, path_to, use_basename=False, workers=workers
        )
    if not os.path.exists(path_to):
        return None
    if to_tar:
        return tar_dir(path_to)
    return path_to


def delete_file_or_dir(
    subpath: str,
    is_file: bool = False,
    workers: int = 0,
    connection_type: V1ConnectionType = None,
):
    connection_type = connection_type or get_artifacts_connection()

    validate_store(connection_type)

    store_path = get_path(connection_type.store_path, subpath)

    store_manager = get_connection_from_type(connection_type=connection_type)
    if is_file:
        store_manager.delete_file(store_path)
    else:
        store_manager.delete(store_path, workers=workers)


def tar_dir(download_path: str) -> str:
    outputs_files = get_files_in_path(download_path)
    tar_base_name = os.path.basename(download_path)
    tar_name = "{}.tar.gz".format(tar_base_name)
    target_path = get_path(settings.CLIENT_CONFIG.archive_root, tar_name)
    create_tarfile(files=outputs_files, tar_path=target_path, relative_to=download_path)
    return target_path
