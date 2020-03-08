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
from polyaxon.connections.schemas.connections import (
    BucketConnectionSchema,
    V1BucketConnection,
    ClaimConnectionSchema,
    V1ClaimConnection,
    HostPathConnectionSchema,
    V1HostPathConnection,
    HostConnectionSchema,
    V1HostConnection,
    GitConnectionSchema,
    V1GitConnection,
    validate_connection,
    ConnectionSchema,
)
from polyaxon.connections.schemas.k8s_resources import (
    validate_k8s_resource,
    V1K8sResourceSchema,
    K8sResourceSchema,
)
