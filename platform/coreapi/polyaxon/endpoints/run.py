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

from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404

from coredb.models.artifacts import ArtifactLineage
from coredb.models.runs import Run
from endpoints.project import ProjectResourceEndpoint
from polycommon.apis.regex import (
    ARTIFACT_NAME_KEY,
    NAME_KEY,
    OWNER_NAME_KEY,
    PROJECT_NAME_KEY,
    RUN_UUID_KEY,
    UUID_KEY,
)


class RunEndpoint(ProjectResourceEndpoint):
    queryset = Run.objects
    lookup_field = UUID_KEY
    lookup_url_kwarg = RUN_UUID_KEY
    CONTEXT_KEYS = (OWNER_NAME_KEY, PROJECT_NAME_KEY, RUN_UUID_KEY)
    CONTEXT_OBJECTS = ("run",)

    def enrich_queryset(self, queryset):
        return queryset.filter(project__name=self.project_name)

    def set_owner(self):
        self.project = self.run.project
        self._owner_id = self.project.owner_id

    def initialize_object_context(self, request: HttpRequest, *args, **kwargs) -> None:
        #  pylint:disable=attribute-defined-outside-init
        self.run = self.get_object()


class RunArtifactListEndpoint(RunEndpoint):
    AUDITOR_EVENT_TYPES = None

    def get_object(self):
        if self._object:
            return self._object

        self._object = get_object_or_404(
            Run, uuid=self.run_uuid, project__name=self.project_name,
        )

        # May raise a permission denied
        self.check_object_permissions(self.request, self._object)

        return self._object

    def enrich_queryset(self, queryset):
        return queryset.filter(run=self.run)


class RunArtifactEndpoint(RunEndpoint):
    AUDITOR_EVENT_TYPES = None
    lookup_field = NAME_KEY
    lookup_url_kwarg = ARTIFACT_NAME_KEY
    CONTEXT_KEYS = (PROJECT_NAME_KEY, RUN_UUID_KEY, ARTIFACT_NAME_KEY)
    CONTEXT_OBJECTS = ("run_artifact",)

    def enrich_queryset(self, queryset):
        return queryset.filter(
            run__uuid=self.run_uuid, run__project__name=self.project_name,
        )

    def set_owner(self):
        self.project = self.run_artifact.run.project
        self._owner_id = self.project.owner_id

    def initialize_object_context(self, request: HttpRequest, *args, **kwargs) -> None:
        #  pylint:disable=attribute-defined-outside-init
        self.run_artifact = self.get_object()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            return queryset.get(artifact__name=self.artifact_name)
        except ArtifactLineage.DoesNotExist:
            raise Http404(
                "No %s matches the given query." % self.queryset.model._meta.object_name
            )
