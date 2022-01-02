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
from typing import Optional

from polyaxon_sdk import V1ConnectionKind

from polyaxon import settings
from polyaxon.connections.reader import get_connection_context_path, get_connection_type
from polyaxon.env_vars.getters import get_artifacts_store_name
from polyaxon.exceptions import PolyaxonStoresException
from polyaxon.schemas.types import V1ConnectionType


def validate_store(connection_type: V1ConnectionType):
    if not connection_type or not connection_type.is_artifact:
        raise PolyaxonStoresException("An artifact store type was not provided.")


def get_artifacts_connection_type() -> Optional[V1ConnectionType]:
    store_name = get_artifacts_store_name()
    if store_name:
        return get_connection_type(store_name)
    if settings.AGENT_CONFIG:
        return settings.AGENT_CONFIG.artifacts_store
    return None


def _get_fs_from_type(
    connection_type: V1ConnectionType,
    asynchronous: bool = False,
    use_listings_cache: bool = False,
    **kwargs
):
    connection_name = connection_type.name if connection_type else None
    context_path = get_connection_context_path(name=connection_name)

    # We assume that `None` refers to local store as well
    if not connection_type or connection_type.kind in {
        V1ConnectionKind.VOLUME_CLAIM,
        V1ConnectionKind.HOST_PATH,
    }:
        from fsspec.implementations.local import LocalFileSystem

        return LocalFileSystem(
            auto_mkdir=kwargs.get("auto_mkdir", True),
            use_listings_cache=use_listings_cache,
        )
    if connection_type.kind == V1ConnectionKind.WASB:
        from polyaxon.fs.azure import get_fs

        return get_fs(
            context_path=context_path,
            asynchronous=asynchronous,
            use_listings_cache=use_listings_cache,
            **kwargs
        )
    if connection_type.kind == V1ConnectionKind.S3:
        from polyaxon.fs.s3 import get_fs

        return get_fs(
            context_path=context_path,
            asynchronous=asynchronous,
            use_listings_cache=use_listings_cache,
            **kwargs
        )
    if connection_type.kind == V1ConnectionKind.GCS:
        from polyaxon.fs.gcs import get_fs

        return get_fs(
            context_path=context_path,
            asynchronous=asynchronous,
            use_listings_cache=use_listings_cache,
            **kwargs
        )


async def get_async_fs_from_type(connection_type: V1ConnectionType, **kwargs):
    fs = _get_fs_from_type(connection_type=connection_type, asynchronous=True, **kwargs)
    if fs.async_impl and hasattr(fs, "set_session"):
        await fs.set_session()
    return fs


def get_sync_fs_from_type(connection_type: V1ConnectionType, **kwargs):
    return _get_fs_from_type(connection_type=connection_type, **kwargs)


def get_fs_from_name(connection_name: str, asynchronous: bool = False, **kwargs):
    connection_type = get_connection_type(connection_name)
    return _get_fs_from_type(
        connection_type=connection_type, asynchronous=asynchronous, **kwargs
    )


async def get_default_fs(**kwargs):
    connection_type = get_artifacts_connection_type()
    return await get_async_fs_from_type(
        connection_type=connection_type, auto_mkdir=True, **kwargs
    )


async def close_fs(fs):
    if hasattr(fs, "close_session"):
        fs.close_session(fs.loop, fs.session)
