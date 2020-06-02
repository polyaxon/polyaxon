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

from coredb.api.artifacts import methods, queries
from coredb.api.artifacts.serializers import (
    RunArtifactNameSerializer,
    RunArtifactSerializer,
)
from coredb.query_managers.artifact import ArtifactQueryManager
from endpoints.run import RunArtifactEndpoint, RunArtifactListEndpoint
from polycommon.apis.filters import OrderingFilter, QueryFilter
from polycommon.apis.paginator import LargeLimitOffsetPagination
from polycommon.apis.regex import RUN_UUID_KEY
from polycommon.endpoints.base import (
    CreateEndpoint,
    DestroyEndpoint,
    ListEndpoint,
    RetrieveEndpoint,
)
from polycommon.events.registry.run import RUN_NEW_ARTIFACTS


class RunArtifactListView(RunArtifactListEndpoint, ListEndpoint, CreateEndpoint):
    queryset = queries.artifacts
    serializer_class = RunArtifactSerializer

    AUDITOR_EVENT_TYPES = {
        "POST": RUN_NEW_ARTIFACTS,
    }
    AUDIT_PROJECT_RESOURCES = True
    PROJECT_RESOURCE_KEY = RUN_UUID_KEY
    AUDIT_EXTRA_KEYS = ("artifacts",)
    AUDIT_INSTANCE = True

    filter_backends = (QueryFilter, OrderingFilter)
    query_manager = ArtifactQueryManager
    check_alive = ArtifactQueryManager.CHECK_ALIVE
    ordering = ArtifactQueryManager.FIELDS_DEFAULT_ORDERING
    ordering_fields = ArtifactQueryManager.FIELDS_ORDERING
    ordering_proxy_fields = ArtifactQueryManager.FIELDS_ORDERING_PROXY

    def create(self, request, *args, **kwargs):
        return methods.create(view=self, request=request, *args, **kwargs)


class RunArtifactNameListView(RunArtifactListEndpoint, ListEndpoint):
    queryset = queries.artifacts_names
    serializer_class = RunArtifactNameSerializer
    pagination_class = LargeLimitOffsetPagination


class RunArtifactDetailView(RunArtifactEndpoint, RetrieveEndpoint, DestroyEndpoint):
    queryset = queries.artifacts
    serializer_class = RunArtifactSerializer
