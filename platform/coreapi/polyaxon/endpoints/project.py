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

from rest_framework.generics import get_object_or_404

from django.http import HttpRequest

from coredb.models.projects import Project
from polycommon.apis.regex import (
    NAME_KEY,
    OWNER_NAME_KEY,
    PROJECT_NAME_KEY,
    PROJECT_OWNER_NAME_KEY,
    UUID_KEY,
)
from polycommon.endpoints.base import BaseEndpoint


class ProjectEndpoint(BaseEndpoint):
    queryset = Project.objects
    lookup_field = NAME_KEY
    lookup_url_kwarg = PROJECT_NAME_KEY
    CONTEXT_KEYS = (OWNER_NAME_KEY, PROJECT_NAME_KEY)
    CONTEXT_OBJECTS = ("project",)

    PROJECT_NAME_KEY = "name"
    PROJECT_OWNER_NAME_KEY = OWNER_NAME_KEY

    def initialize_object_context(self, request: HttpRequest, *args, **kwargs) -> None:
        #  pylint:disable=attribute-defined-outside-init
        self.project = self.get_object()

    def set_owner(self):
        self._owner_id = self.project.owner.id


class ProjectResourceListEndpoint(ProjectEndpoint):
    AUDITOR_EVENT_TYPES = None

    def get_object(self):
        if self._object:
            return self._object
        self._object = get_object_or_404(Project, name=self.project_name,)
        return self._object

    def enrich_queryset(self, queryset):
        return queryset.filter(project=self.project)


class ProjectResourceEndpoint(ProjectEndpoint):
    AUDITOR_EVENT_TYPES = None
    lookup_field = UUID_KEY

    PROJECT_NAME_KEY = PROJECT_NAME_KEY
    PROJECT_OWNER_NAME_KEY = PROJECT_OWNER_NAME_KEY
