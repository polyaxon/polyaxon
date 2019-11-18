#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

from __future__ import absolute_import

# flake8: noqa

# import apis into api package
from polyaxon_sdk.api.agents_v1_api import AgentsV1Api
from polyaxon_sdk.api.artifacts_stores_v1_api import ArtifactsStoresV1Api
from polyaxon_sdk.api.auth_v1_api import AuthV1Api
from polyaxon_sdk.api.git_accesses_v1_api import GitAccessesV1Api
from polyaxon_sdk.api.k8s_config_maps_v1_api import K8sConfigMapsV1Api
from polyaxon_sdk.api.k8s_secrets_v1_api import K8sSecretsV1Api
from polyaxon_sdk.api.projects_v1_api import ProjectsV1Api
from polyaxon_sdk.api.queues_v1_api import QueuesV1Api
from polyaxon_sdk.api.registry_accesses_v1_api import RegistryAccessesV1Api
from polyaxon_sdk.api.runs_v1_api import RunsV1Api
from polyaxon_sdk.api.search_v1_api import SearchV1Api
from polyaxon_sdk.api.users_v1_api import UsersV1Api
from polyaxon_sdk.api.versions_v1_api import VersionsV1Api
