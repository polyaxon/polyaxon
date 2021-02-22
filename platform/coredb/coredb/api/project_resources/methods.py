#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

from rest_framework import status
from rest_framework.response import Response

from coredb.abstracts.getter import get_run_model
from coredb.api.base.tags import TagsMixin
from coredb.managers.statuses import bulk_new_run_status
from polyaxon.lifecycle import LifeCycle, V1StatusCondition, V1Statuses
from polycommon import auditor, live_state
from polycommon.events.registry.run import (
    RUN_APPROVED_ACTOR,
    RUN_DELETED_ACTOR,
    RUN_STOPPED_ACTOR,
)


def create_runs_tags(view, request, *args, **kwargs):
    tags = request.data.get("tags", [])
    if not tags:
        return Response(status=status.HTTP_200_OK, data={})

    updated = []
    run_model = get_run_model()
    for run in run_model.all.filter(
        project=view.project, uuid__in=request.data.get("uuids", [])
    ).only("id", "tags"):
        run.tags = TagsMixin.validated_tags({"tags": tags, "merge": True}, run.tags)[
            "tags"
        ]
        updated.append(run)

        run_model.objects.bulk_update(updated, ["tags"])
    return Response(status=status.HTTP_200_OK, data={})


def stop_runs(view, request, actor, *args, **kwargs):
    # Immediate stop
    queryset = (
        get_run_model()
        .objects.filter(project=view.project, uuid__in=request.data.get("uuids", []))
        .filter(status__in=LifeCycle.SAFE_STOP_VALUES)
    )
    condition = V1StatusCondition.get_condition(
        type=V1Statuses.STOPPED,
        status="True",
        reason="EventHandler",
        message="User requested to stop the run.",
    )
    bulk_new_run_status(queryset, condition)

    queryset = (
        get_run_model()
        .objects.filter(project=view.project, uuid__in=request.data.get("uuids", []))
        .exclude(status__in=LifeCycle.DONE_OR_IN_PROGRESS_VALUES)
    )
    runs = [r for r in queryset]
    condition = V1StatusCondition.get_condition(
        type=V1Statuses.STOPPING,
        status="True",
        reason="EventHandler",
        message="User requested to stop the run.",
    )
    bulk_new_run_status(runs, condition)
    for run in runs:
        auditor.record(
            event_type=RUN_STOPPED_ACTOR,
            instance=run,
            actor_id=actor.id,
            actor_name=actor.username,
            owner_id=view.project.owner_id,
            owner_name=view.owner_name,
            project_name=view.project_name,
        )

    return Response(status=status.HTTP_200_OK, data={})


def approve_runs(view, request, actor, *args, **kwargs):
    queryset = (
        get_run_model()
        .objects.filter(project=view.project, uuid__in=request.data.get("uuids", []))
        .exclude(is_approved=True)
    )
    runs = [r for r in queryset]
    queryset.update(is_approved=True)
    for run in runs:
        auditor.record(
            event_type=RUN_APPROVED_ACTOR,
            instance=run,
            actor_id=actor.id,
            actor_name=actor.username,
            owner_id=view.project.owner_id,
            owner_name=view.owner_name,
            project_name=view.project_name,
        )

    return Response(status=status.HTTP_200_OK, data={})


def delete_runs(view, request, actor, *args, **kwargs):
    runs = get_run_model().objects.filter(
        project=view.project, uuid__in=request.data.get("uuids", [])
    )
    for run in runs:
        auditor.record(
            event_type=RUN_DELETED_ACTOR,
            instance=run,
            actor_id=actor.id,
            actor_name=actor.username,
            owner_id=view.project.owner_id,
            owner_name=view.owner_name,
            project_name=view.project_name,
        )
    # Delete non managed immediately
    runs.filter(is_managed=False).delete()
    # Deletion in progress
    runs.filter(is_managed=True).update(
        live_state=live_state.STATE_DELETION_PROGRESSING
    )
    return Response(status=status.HTTP_200_OK, data={})
