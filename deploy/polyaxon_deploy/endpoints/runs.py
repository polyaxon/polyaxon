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

from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from polyaxon import settings
from polyaxon.api import API_V1_LOCATION
from polyaxon_deploy.endpoints.base import ConfigResponse


async def get_run_details(request: Request) -> Response:
    run_uuid = request.path_params["run_uuid"]
    offline_path = os.path.join(
        settings.SANDBOX_CONFIG.store_root, run_uuid, "run_data.json"
    )

    with open(offline_path, "r") as config_file:
        config_str = config_file.read()
    return ConfigResponse(config_str)


async def get_run_lineage(request: Request) -> Response:
    run_uuid = request.path_params["run_uuid"]
    offline_path = os.path.join(
        settings.SANDBOX_CONFIG.store_root, run_uuid, "run_data.json"
    )

    with open(offline_path, "r") as config_file:
        config_str = config_file.read()
    return ConfigResponse(config_str)


async def get_run_artifact_lineage(request: Request) -> Response:
    run_uuid = request.path_params["run_uuid"]
    offline_path = os.path.join(
        settings.SANDBOX_CONFIG.store_root, run_uuid, "lineages.json"
    )

    with open(offline_path, "r") as config_file:
        config_str = config_file.read()
        config_str = f'{{"results": {config_str}}}'

    return ConfigResponse(config_str)


URLS_RUNS_DETAILS = API_V1_LOCATION + "{owner:str}/{project:str}/runs/{run_uuid:str}/"
URLS_RUNS_STATUSES = (
    API_V1_LOCATION + "{owner:str}/{project:str}/runs/{run_uuid:str}/statuses"
)
URLS_RUNS_LINEAGE_ARTIFACTS = (
    API_V1_LOCATION + "{owner:str}/{project:str}/runs/{run_uuid:str}/lineage/artifacts"
)

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
]
