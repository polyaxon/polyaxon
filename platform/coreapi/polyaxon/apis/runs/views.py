#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from django.http import Http404

from coredb import operations
from coredb.api.runs import methods
from coredb.api.runs.serializers import (
    RunDetailSerializer,
    RunSerializer,
    RunStatusSerializer,
)
from coredb.models.runs import Run
from coredb.queries.runs import STATUS_UPDATE_COLUMNS_DEFER
from endpoints.run import RunEndpoint
from polyaxon.lifecycle import LifeCycle
from polycommon import conf
from polycommon.apis.regex import RUN_UUID_KEY
from polycommon.endpoints.base import (
    CreateEndpoint,
    DestroyEndpoint,
    RetrieveEndpoint,
    UpdateEndpoint,
)
from polycommon.events.registry.run import (
    RUN_APPROVED_ACTOR,
    RUN_COPIED_ACTOR,
    RUN_DELETED_ACTOR,
    RUN_RESTARTED_ACTOR,
    RUN_RESUMED_ACTOR,
    RUN_STOPPED_ACTOR,
)
from polycommon.options.registry.k8s import K8S_NAMESPACE


class RunDetailView(RunEndpoint, RetrieveEndpoint, DestroyEndpoint, UpdateEndpoint):
    queryset = Run.all.select_related("original", "project")
    serializer_class = RunDetailSerializer
    AUDITOR_EVENT_TYPES = {
        "DELETE": RUN_DELETED_ACTOR,
    }
    AUDIT_PROJECT_RESOURCES = True
    PROJECT_RESOURCE_KEY = RUN_UUID_KEY
    AUDIT_INSTANCE = True

    def perform_destroy(self, instance):
        # Deletion managed by the handler
        pass


class RunCloneView(RunEndpoint, CreateEndpoint):
    serializer_class = RunSerializer
    AUDIT_PROJECT_RESOURCES = True
    PROJECT_RESOURCE_KEY = RUN_UUID_KEY
    AUDIT_INSTANCE = True

    def clone(self, obj, content, **kwargs):
        pass

    def pre_validate(self, obj):
        return obj

    def post(self, request, *args, **kwargs):
        return methods.clone_run(view=self, request=request, *args, **kwargs)


class RunRestartView(RunCloneView):
    AUDITOR_EVENT_TYPES = {"POST": RUN_RESTARTED_ACTOR}

    def clone(self, obj, content, **kwargs):
        return operations.restart_run(
            run=obj,
            user_id=self.request.user.id,
            content=content,
            name=kwargs.get("name"),
            description=kwargs.get("description"),
            tags=kwargs.get("tags"),
        )


class RunResumeView(RunCloneView):
    AUDITOR_EVENT_TYPES = {"POST": RUN_RESUMED_ACTOR}

    def clone(self, obj, content, **kwargs):
        return operations.resume_run(
            run=obj,
            user_id=self.request.user.id,
            content=content,
            message="Run was resumed by user.",
        )

    def pre_validate(self, obj):
        if not LifeCycle.is_done(obj.status):
            raise ValidationError(
                "Cannot resume this run, the run must reach a final state first, "
                "current status error: {}".format(obj.status)
            )
        return super().pre_validate(obj)


class RunCopyView(RunCloneView):
    AUDITOR_EVENT_TYPES = {"POST": RUN_COPIED_ACTOR}

    def clone(self, obj, content, **kwargs):
        return operations.copy_run(
            run=obj,
            user_id=self.request.user.id,
            content=content,
            name=kwargs.get("name"),
            description=kwargs.get("description"),
            tags=kwargs.get("tags"),
            meta_info=kwargs.get("meta_info"),
        )


class RunStatusListView(RunEndpoint, RetrieveEndpoint, CreateEndpoint):
    queryset = Run.restorable.defer(*STATUS_UPDATE_COLUMNS_DEFER).select_related(
        "project",
    )
    serializer_class = RunStatusSerializer

    def perform_create(self, serializer):
        try:
            methods.create_status(view=self, serializer=serializer)
        except Run.DoesNotExit:
            raise Http404


class RunStopView(RunEndpoint, CreateEndpoint):
    AUDITOR_EVENT_TYPES = {"POST": RUN_STOPPED_ACTOR}
    AUDIT_PROJECT_RESOURCES = True
    PROJECT_RESOURCE_KEY = RUN_UUID_KEY
    AUDIT_INSTANCE = True

    def post(self, request, *args, **kwargs):
        return methods.stop_run(view=self, request=request, *args, **kwargs)


class RunApproveView(RunEndpoint, CreateEndpoint):
    AUDITOR_EVENT_TYPES = {"POST": RUN_APPROVED_ACTOR}
    AUDIT_PROJECT_RESOURCES = True
    PROJECT_RESOURCE_KEY = RUN_UUID_KEY
    AUDIT_INSTANCE = True

    def post(self, request, *args, **kwargs):
        return methods.approve_run(view=self, request=request, *args, **kwargs)


class RunNamespaceView(RunEndpoint, RetrieveEndpoint):
    def retrieve(self, request, *args, **kwargs):
        namespace = {"namespace": conf.get(K8S_NAMESPACE)}
        return Response(namespace)
