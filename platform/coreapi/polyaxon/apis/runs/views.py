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

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from coredb.api.runs import methods, queries
from coredb.api.runs.serializers import (
    RunDetailSerializer,
    RunSerializer,
    RunStatusSerializer,
)
from coredb.managers.runs import copy_run, restart_run, resume_run
from coredb.models.runs import Run
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
    RUN_COPIED_ACTOR,
    RUN_DELETED_ACTOR,
    RUN_RESTARTED_ACTOR,
    RUN_RESUMED_ACTOR,
    RUN_STOPPED_ACTOR,
)
from polycommon.options.registry.k8s import K8S_NAMESPACE


class RunDetailView(RunEndpoint, RetrieveEndpoint, DestroyEndpoint, UpdateEndpoint):
    queryset = queries.single_run
    serializer_class = RunDetailSerializer
    AUDITOR_EVENT_TYPES = {
        "DELETE": RUN_DELETED_ACTOR,
    }
    AUDIT_PROJECT_RESOURCES = True
    PROJECT_RESOURCE_KEY = RUN_UUID_KEY
    AUDIT_INSTANCE = True

    def perform_destroy(self, instance):
        instance.archive()


class RunCloneView(RunEndpoint, CreateEndpoint):
    queryset = queries.single_run
    serializer_class = RunSerializer
    AUDIT_PROJECT_RESOURCES = True
    PROJECT_RESOURCE_KEY = RUN_UUID_KEY
    AUDIT_INSTANCE = True

    def clone(self, obj, content):
        pass

    def pre_validate(self, obj):
        pass

    def post(self, request, *args, **kwargs):
        return methods.clone_run(view=self, request=request, *args, **kwargs)


class RunRestartView(RunCloneView):
    AUDITOR_EVENT_TYPES = {"POST": RUN_RESTARTED_ACTOR}

    def clone(self, obj, content):
        return restart_run(run=obj, user_id=self.request.user.id, content=content)


class RunResumeView(RunCloneView):
    AUDITOR_EVENT_TYPES = {"POST": RUN_RESUMED_ACTOR}

    def clone(self, obj, content):
        return resume_run(run=obj, user_id=self.request.user.id, content=content)

    def pre_validate(self, obj):
        if not LifeCycle.is_done(obj.status):
            raise ValidationError(
                "Cannot resume this run, the run must reach a final state first, "
                "current status error: {}".format(obj.status)
            )


class RunCopyView(RunCloneView):
    AUDITOR_EVENT_TYPES = {"POST": RUN_COPIED_ACTOR}

    def clone(self, obj, content):
        return copy_run(run=obj, user_id=self.request.user.id, content=content)


class RunStatusListView(RunEndpoint, RetrieveEndpoint, CreateEndpoint):
    queryset = Run.objects.only("status_conditions", "status").prefetch_related(
        "project",
    )
    serializer_class = RunStatusSerializer

    def perform_create(self, serializer):
        methods.create_status(view=self, serializer=serializer)


class RunStopView(RunEndpoint, CreateEndpoint):
    queryset = queries.deferred_runs

    AUDITOR_EVENT_TYPES = {"POST": RUN_STOPPED_ACTOR}
    AUDIT_PROJECT_RESOURCES = True
    PROJECT_RESOURCE_KEY = RUN_UUID_KEY
    AUDIT_INSTANCE = True

    def post(self, request, *args, **kwargs):
        return methods.stop_run(view=self, request=request, *args, **kwargs)


class RunNamespaceView(RunEndpoint, RetrieveEndpoint):
    def retrieve(self, request, *args, **kwargs):
        namespace = {"namespace": conf.get(K8S_NAMESPACE)}
        return Response(namespace)
