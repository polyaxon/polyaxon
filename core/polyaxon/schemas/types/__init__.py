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

from polyaxon.schemas.types.artifacts import ArtifactsTypeSchema, V1ArtifactsType
from polyaxon.schemas.types.auth import AuthTypeSchema, V1AuthType
from polyaxon.schemas.types.connections import ConnectionTypeSchema, V1ConnectionType
from polyaxon.schemas.types.dockerfile import DockerfileTypeSchema, V1DockerfileType
from polyaxon.schemas.types.file import FileTypeSchema, V1FileType
from polyaxon.schemas.types.gcs import GcsTypeSchema, V1GcsType
from polyaxon.schemas.types.git import GitTypeSchema, V1GitType
from polyaxon.schemas.types.k8s_resources import (
    K8sResourceTypeSchema,
    V1K8sResourceType,
)
from polyaxon.schemas.types.s3 import S3TypeSchema, V1S3Type
from polyaxon.schemas.types.uri import UriTypeSchema, V1UriType
from polyaxon.schemas.types.wasb import V1WasbType, WasbTypeSchema
