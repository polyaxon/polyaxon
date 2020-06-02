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
from rest_framework.generics import CreateAPIView

from coredb.api.projects import queries
from coredb.api.projects.serializers import (
    ProjectCreateSerializer,
    ProjectDetailSerializer,
    ProjectNameSerializer,
    ProjectSerializer,
)
from coredb.models.projects import Project
from coredb.query_managers.project import ProjectQueryManager
from endpoints.project import ProjectEndpoint
from polycommon.apis.filters import OrderingFilter, QueryFilter
from polycommon.apis.paginator import LargeLimitOffsetPagination
from polycommon.endpoints.base import (
    BaseEndpoint,
    DestroyEndpoint,
    ListEndpoint,
    RetrieveEndpoint,
    UpdateEndpoint,
)


class ProjectCreateView(BaseEndpoint, CreateAPIView):
    serializer_class = ProjectCreateSerializer


class ProjectListView(BaseEndpoint, ListEndpoint):
    queryset = queries.projects.order_by("-updated_at")
    serializer_class = ProjectSerializer

    filter_backends = (QueryFilter, OrderingFilter)
    query_manager = ProjectQueryManager
    check_alive = ProjectQueryManager.CHECK_ALIVE
    ordering = ProjectQueryManager.FIELDS_DEFAULT_ORDERING
    ordering_fields = ProjectQueryManager.FIELDS_ORDERING
    ordering_proxy_fields = ProjectQueryManager.FIELDS_ORDERING_PROXY


class ProjectNameListView(BaseEndpoint, ListEndpoint):
    queryset = Project.objects.only("name").order_by("-updated_at")
    serializer_class = ProjectNameSerializer
    pagination_class = LargeLimitOffsetPagination


class ProjectDetailView(
    ProjectEndpoint, RetrieveEndpoint, UpdateEndpoint, DestroyEndpoint
):
    queryset = queries.project_detail
    serializer_class = ProjectDetailSerializer
