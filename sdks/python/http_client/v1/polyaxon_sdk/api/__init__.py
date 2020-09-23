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

from __future__ import absolute_import

# flake8: noqa

# import apis into api package
from polyaxon_sdk.api.agents_v1_api import AgentsV1Api
from polyaxon_sdk.api.artifacts_stores_v1_api import ArtifactsStoresV1Api
from polyaxon_sdk.api.auth_v1_api import AuthV1Api
from polyaxon_sdk.api.component_hub_v1_api import ComponentHubV1Api
from polyaxon_sdk.api.connections_v1_api import ConnectionsV1Api
from polyaxon_sdk.api.dashboards_v1_api import DashboardsV1Api
from polyaxon_sdk.api.model_registry_v1_api import ModelRegistryV1Api
from polyaxon_sdk.api.organizations_v1_api import OrganizationsV1Api
from polyaxon_sdk.api.presets_v1_api import PresetsV1Api
from polyaxon_sdk.api.project_dashboards_v1_api import ProjectDashboardsV1Api
from polyaxon_sdk.api.project_searches_v1_api import ProjectSearchesV1Api
from polyaxon_sdk.api.projects_v1_api import ProjectsV1Api
from polyaxon_sdk.api.queues_v1_api import QueuesV1Api
from polyaxon_sdk.api.runs_v1_api import RunsV1Api
from polyaxon_sdk.api.schemas_v1_api import SchemasV1Api
from polyaxon_sdk.api.searches_v1_api import SearchesV1Api
from polyaxon_sdk.api.teams_v1_api import TeamsV1Api
from polyaxon_sdk.api.users_v1_api import UsersV1Api
from polyaxon_sdk.api.versions_v1_api import VersionsV1Api
