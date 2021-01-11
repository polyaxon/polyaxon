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

from polyaxon_sdk import V1ConnectionKind

from polyaxon.connections.reader import get_connection_type
from polyaxon.schemas.types import V1ConnectionType


def get_connection_from_type(connection_type: V1ConnectionType, **kwargs):
    # We assume that `None` refers to local store as well
    if not connection_type or connection_type.kind in {
        V1ConnectionKind.VOLUME_CLAIM,
        V1ConnectionKind.HOST_PATH,
    }:
        from polyaxon.stores.local_store import LocalStore

        return LocalStore()
    if connection_type.kind == V1ConnectionKind.WASB:
        from polyaxon.connections.azure.azure_blobstore import AzureBlobStoreService

        return AzureBlobStoreService(connection_name=connection_type.name, **kwargs)
    if connection_type.kind == V1ConnectionKind.S3:
        from polyaxon.connections.aws.s3 import S3Service

        return S3Service(connection_name=connection_type.name, **kwargs)
    if connection_type.kind == V1ConnectionKind.GCS:
        from polyaxon.connections.gcp.gcs import GCSService

        return GCSService(connection_name=connection_type.name, **kwargs)


def get_connection_from_name(connection_name: str, **kwargs):
    connection_type = get_connection_type(connection_name)
    return get_connection_from_type(connection_type=connection_type, **kwargs)
