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

from polyaxon_schemas.defs.types.artifacts import ArtifactsTypeSchema, V1ArtifactsType
from polyaxon_schemas.defs.types.auth import AuthTypeSchema, V1AuthType
from polyaxon_schemas.defs.types.connections import ConnectionTypeSchema, V1ConnectionType
from polyaxon_schemas.defs.types.dockerfile import DockerfileTypeSchema, V1DockerfileType
from polyaxon_schemas.defs.types.event import EventSchema, V1EventType
from polyaxon_schemas.defs.types.file import FileTypeSchema, V1FileType
from polyaxon_schemas.defs.types.gcs import GcsTypeSchema, V1GcsType
from polyaxon_schemas.defs.types.git import GitTypeSchema, V1GitType
from polyaxon_schemas.defs.types.k8s_resources import (
    K8sResourceTypeSchema,
    V1K8sResourceType,
)
from polyaxon_schemas.defs.types.s3 import S3TypeSchema, V1S3Type
from polyaxon_schemas.defs.types.uri import UriTypeSchema, V1UriType
from polyaxon_schemas.defs.types.wasb import V1WasbType, WasbTypeSchema
from polyaxon_schemas.defs.types.dockerfile import V1DockerfileType, DockerfileTypeSchema, POLYAXON_DOCKERFILE_NAME, POLYAXON_DOCKER_WORKDIR, POLYAXON_DOCKER_SHELL
