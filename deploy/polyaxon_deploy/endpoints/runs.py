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
import os

from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from polyaxon import settings
from polyaxon.api import API_V1_LOCATION
from polyaxon.contexts import paths as ctx_paths
from polyaxon_deploy.endpoints.base import ConfigResponse, UJSONResponse


async def get_run_details(request: Request) -> Response:
    run_uuid = request.path_params["run_uuid"]
    data_path = os.path.join(
        settings.SANDBOX_CONFIG.store_root,
        run_uuid,
        ctx_paths.CONTEXT_LOCAL_RUN,
    )
    if not os.path.exists(data_path) or not os.path.isfile(data_path):
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    with open(data_path, "r") as config_file:
        config_str = config_file.read()
    return ConfigResponse(config_str)


async def get_run_artifact_lineage(request: Request) -> Response:
    run_uuid = request.path_params["run_uuid"]
    data_path = os.path.join(
        settings.SANDBOX_CONFIG.store_root,
        run_uuid,
        ctx_paths.CONTEXT_LOCAL_LINEAGES,
    )
    if not os.path.exists(data_path) or not os.path.isfile(data_path):
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    with open(data_path, "r") as config_file:
        config_str = config_file.read()
        config_str = f'{{"results": {config_str}}}'

    return ConfigResponse(config_str)


async def list_runs(request: Request) -> Response:
    data_path = os.path.join(settings.SANDBOX_CONFIG.store_root, "runs")
    if not os.path.exists(data_path) or not os.path.isdir(data_path):
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    data = []
    for run in os.listdir(data_path):
        run_path = os.path.join(data_path, run, ctx_paths.CONTEXT_LOCAL_RUN)
        if not os.path.exists(run_path) or not os.path.isfile(run_path):
            continue

        with open(run_path, "r") as config_file:
            data.append(config_file.read())
    data_str = ",".join(data)
    config_str = f'{{"results": [{data_str}], "count": {len(data)}}}'
    return ConfigResponse(config_str)


async def get_project_details(request: Request) -> Response:
    return UJSONResponse({"name": "demo"})


URLS_RUNS_DETAILS = API_V1_LOCATION + "{owner:str}/{project:str}/runs/{run_uuid:str}/"
URLS_RUNS_STATUSES = (
    API_V1_LOCATION + "{owner:str}/{project:str}/runs/{run_uuid:str}/statuses"
)
URLS_RUNS_LINEAGE_ARTIFACTS = (
    API_V1_LOCATION + "{owner:str}/{project:str}/runs/{run_uuid:str}/lineage/artifacts"
)
URLS_RUNS_LIST = API_V1_LOCATION + "{owner:str}/{project:str}/runs/"
URLS_PROJECTS_DETAILS = API_V1_LOCATION + "{owner:str}/{project:str}/"

# fmt: off
runs_routes = [
    Route(
        URLS_RUNS_DETAILS,
        get_run_details,
        name="get_run_details",
        methods=["GET"],
    ),
    Route(
        URLS_RUNS_STATUSES,
        get_run_details,
        name="get_run_details",
        methods=["GET"],
    ),
    Route(
        URLS_RUNS_LINEAGE_ARTIFACTS,
        get_run_artifact_lineage,
        name="get_run_artifact_lineage",
        methods=["GET"],
    ),
    Route(
        URLS_RUNS_LIST,
        list_runs,
        name="list_runs",
        methods=["GET"],
    ),
    Route(
        URLS_PROJECTS_DETAILS,
        get_project_details,
        name="get_project_details",
        methods=["GET"],
    ),
]
