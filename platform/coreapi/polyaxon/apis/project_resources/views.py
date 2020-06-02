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

from coredb.api.artifacts import queries as runs_artifacts_queries
from coredb.api.artifacts.serializers import RunArtifactLightSerializer
from coredb.api.project_resources import methods
from coredb.api.project_resources import queries as runs_queries
from coredb.api.project_resources.serializers import (
    OperationCreateSerializer,
    RunSerializer,
)
from coredb.query_managers.artifact import ArtifactQueryManager
from coredb.query_managers.run import RunQueryManager
from endpoints.project import ProjectResourceListEndpoint
from polycommon.apis.filters import OrderingFilter, QueryFilter
from polycommon.endpoints.base import (
    CreateEndpoint,
    DestroyEndpoint,
    ListEndpoint,
    PostEndpoint,
)


class ProjectRunsTagView(ProjectResourceListEndpoint, PostEndpoint):
    def post(self, request, *args, **kwargs):
        return methods.create_runs_tags(view=self, request=request, *args, **kwargs)


class ProjectRunsStopView(ProjectResourceListEndpoint, PostEndpoint):
    def post(self, request, *args, **kwargs):
        return methods.stop_runs(
            view=self, request=request, actor=self.project.actor, *args, **kwargs
        )


class ProjectRunsDeleteView(ProjectResourceListEndpoint, DestroyEndpoint):
    def delete(self, request, *args, **kwargs):
        return methods.delete_runs(
            view=self, request=request, actor=self.project.actor, *args, **kwargs
        )


class ProjectRunsListView(ProjectResourceListEndpoint, ListEndpoint, CreateEndpoint):
    queryset = runs_queries.runs
    filter_backends = (QueryFilter, OrderingFilter)
    query_manager = RunQueryManager
    check_alive = RunQueryManager.CHECK_ALIVE
    ordering = RunQueryManager.FIELDS_DEFAULT_ORDERING
    ordering_fields = RunQueryManager.FIELDS_ORDERING
    ordering_proxy_fields = RunQueryManager.FIELDS_ORDERING_PROXY
    serializer_class_mapping = {
        "GET": RunSerializer,
        "POST": OperationCreateSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(project=self.project)


class ProjectRunsArtifactsView(ProjectResourceListEndpoint, ListEndpoint):

    queryset = runs_artifacts_queries.project_runs_artifacts
    serializer_class = RunArtifactLightSerializer
    filter_backends = (QueryFilter, OrderingFilter)
    query_manager = ArtifactQueryManager
    check_alive = ArtifactQueryManager.CHECK_ALIVE
    ordering = ArtifactQueryManager.FIELDS_DEFAULT_ORDERING
    ordering_fields = ArtifactQueryManager.FIELDS_ORDERING
    ordering_proxy_fields = ArtifactQueryManager.FIELDS_ORDERING_PROXY

    def enrich_queryset(self, queryset):
        return queryset.filter(run__project=self.project)
