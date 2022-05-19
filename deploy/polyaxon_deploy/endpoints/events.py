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

from typing import Set

from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from polyaxon.api import STREAMS_V1_LOCATION
from polyaxon.utils.bool_utils import to_bool
from polyaxon_deploy.connections.fs import AppFS
from polyaxon_deploy.controllers.events import (
    get_archived_operation_events,
    get_archived_operation_events_and_assets,
    get_archived_operation_resources,
    get_archived_operations_events,
)
from polyaxon_deploy.endpoints.base import UJSONResponse
from polyaxon_deploy.endpoints.utils import redirect_file
from traceml.artifacts import V1ArtifactKind
from traceml.events import V1Events
from traceml.processors.importance_processors import calculate_importance_correlation


async def get_multi_run_events(request: Request) -> UJSONResponse:
    event_kind = request.path_params["event_kind"]
    force = to_bool(request.query_params.get("force"), handle_none=True)
    if event_kind not in V1ArtifactKind.allowable_values:
        raise HTTPException(
            detail="received an unrecognisable event {}.".format(event_kind),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    run_uuids = request.query_params["runs"]
    event_names = request.query_params["names"]
    orient = request.query_params.get("orient")
    sample = request.query_params.get("sample")
    orient = orient or V1Events.ORIENT_DICT
    event_names = {e for e in event_names.split(",") if e} if event_names else set([])
    run_uuids = {e for e in run_uuids.split(",") if e} if run_uuids else set([])
    events = await get_archived_operations_events(
        fs=await AppFS.get_fs(),
        run_uuids=run_uuids,
        event_kind=event_kind,
        event_names=event_names,
        orient=orient,
        check_cache=not force,
        sample=sample,
    )
    return UJSONResponse({"data": events})


async def get_package_event_assets(
    run_uuid: str, event_kind: str, event_names: Set[str], force: bool
) -> Response:
    archived_path = await get_archived_operation_events_and_assets(
        fs=await AppFS.get_fs(),
        run_uuid=run_uuid,
        event_kind=event_kind,
        event_names=event_names,
        check_cache=not force,
    )
    if not archived_path:
        return Response(
            content="Artifact not found: filepath={}".format(archived_path),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return await redirect_file(archived_path)


async def get_run_events(request: Request) -> UJSONResponse:
    run_uuid = request.path_params["run_uuid"]
    event_kind = request.path_params["event_kind"]
    force = to_bool(request.query_params.get("force"), handle_none=True)
    pkg_assets = to_bool(request.query_params.get("pkg_assets"), handle_none=True)
    if event_kind not in V1ArtifactKind.allowable_values:
        raise HTTPException(
            detail="received an unrecognisable event {}.".format(event_kind),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    event_names = request.query_params["names"]
    orient = request.query_params.get("orient")
    sample = request.query_params.get("sample")
    orient = orient or V1Events.ORIENT_DICT
    event_names = {e for e in event_names.split(",") if e} if event_names else set([])
    if pkg_assets:
        return await get_package_event_assets(
            run_uuid=run_uuid,
            event_kind=event_kind,
            event_names=event_names,
            force=force,
        )
    events = await get_archived_operation_events(
        fs=await AppFS.get_fs(),
        run_uuid=run_uuid,
        event_kind=event_kind,
        event_names=event_names,
        orient=orient,
        check_cache=not force,
        sample=sample,
    )
    return UJSONResponse({"data": events})


async def get_run_resources(request: Request) -> UJSONResponse:
    run_uuid = request.path_params["run_uuid"]
    event_names = request.query_params.get("names")
    orient = request.query_params.get("orient")
    force = to_bool(request.query_params.get("force"), handle_none=True)
    sample = request.query_params.get("sample")
    orient = orient or V1Events.ORIENT_DICT
    event_names = {e for e in event_names.split(",") if e} if event_names else set([])
    events = await get_archived_operation_resources(
        fs=await AppFS.get_fs(),
        run_uuid=run_uuid,
        event_kind=V1ArtifactKind.METRIC,
        event_names=event_names,
        orient=orient,
        check_cache=not force,
        sample=sample,
    )
    return UJSONResponse({"data": events})


async def get_run_importance_correlation(request: Request) -> UJSONResponse:
    body = await request.json()
    data = body.get("data")
    data = data or {}
    params = data.get("params")
    metrics = data.get("metrics")
    return UJSONResponse(
        {"data": calculate_importance_correlation(metrics=metrics, params=params)}
    )


URLS_RUNS_MULTI_EVENTS = (
    STREAMS_V1_LOCATION
    + "{namespace:str}/{owner:str}/{project:str}/runs/multi/events/{event_kind:str}"
)
URLS_RUNS_EVENTS = (
    STREAMS_V1_LOCATION + "{namespace:str}/{owner:str}/{project:str}/runs/"
    "{run_uuid:str}/events/{event_kind:str}"
)
URLS_RUNS_RESOURCES = (
    STREAMS_V1_LOCATION + "{namespace:str}/{owner:str}/{project:str}/runs/"
    "{run_uuid:str}/resources"
)
URLS_RUNS_IMPORTANCE_CORRELATION = (
    STREAMS_V1_LOCATION + "{namespace:str}/{owner:str}/{project:str}/runs/"
    "{run_uuid:str}/importance"
)

# fmt: off
events_routes = [
    Route(
        URLS_RUNS_MULTI_EVENTS,
        get_multi_run_events,
        name="multi_run_events",
        methods=["GET"],
    ),
    Route(
        URLS_RUNS_RESOURCES,
        get_run_resources,
        name="resources",
        methods=["GET"],
    ),
    Route(
        URLS_RUNS_IMPORTANCE_CORRELATION,
        get_run_importance_correlation,
        name="resources",
        methods=["POST"],
    ),
    Route(
        URLS_RUNS_EVENTS,
        get_run_events,
        name="events",
        methods=["GET"],
    ),
]
