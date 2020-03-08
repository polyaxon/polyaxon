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

from polyaxon.schemas.types.dockerfile import V1DockerfileType, DockerfileTypeSchema
from polyaxon.schemas.types.artifacts import V1ArtifactsType, ArtifactsTypeSchema
from polyaxon.schemas.types.auth import V1AuthType, AuthTypeSchema
from polyaxon.schemas.types.k8s_resources import (
    V1K8sResourceType,
    K8sResourceTypeSchema,
)
from polyaxon.schemas.types.connections import V1ConnectionType, ConnectionTypeSchema
from polyaxon.schemas.types.gcs import V1GcsType, GcsTypeSchema
from polyaxon.schemas.types.git import V1GitType, GitTypeSchema
from polyaxon.schemas.types.s3 import V1S3Type, S3TypeSchema
from polyaxon.schemas.types.uri import V1UriType, UriTypeSchema
from polyaxon.schemas.types.wasb import V1WasbType, WasbTypeSchema
