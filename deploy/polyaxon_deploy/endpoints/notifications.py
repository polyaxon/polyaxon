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

from starlette import status
from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from polyaxon import settings
from polyaxon.api import STREAMS_V1_LOCATION
from polyaxon.lifecycle import V1StatusCondition
from polyaxon_deploy.endpoints.base import UJSONResponse
from polyaxon_deploy.logger import logger
from polyaxon_deploy.tasks.notification import notify_run


async def notify(request: Request) -> Response:
    namespace = request.path_params["namespace"]
    owner = request.path_params["owner"]
    project = request.path_params["project"]
    run_uuid = request.path_params["run_uuid"]
    body = await request.json()
    run_name = body.get("name")
    condition = body.get("condition")
    if not condition:
        errors = "Received a notification request without condition."
        logger.warning(errors)
        return UJSONResponse(
            content={"errors": errors},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    condition = V1StatusCondition.get_condition(**condition)
    connections = body.get("connections")
    if not connections:
        errors = "Received a notification request without connections."
        logger.warning(errors)
        return UJSONResponse(
            content={"errors": errors},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if not settings.AGENT_CONFIG.connections:
        errors = "Received a notification request, but the agent did not declare connections."
        logger.warning(errors)
        return UJSONResponse(
            content={"errors": errors},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    task = BackgroundTask(
        notify_run,
        namespace=namespace,
        owner=owner,
        project=project,
        run_uuid=run_uuid,
        run_name=run_name,
        condition=condition,
        connections=connections,
    )
    return Response(background=task)


URLS_RUNS_NOTIFY = (
    STREAMS_V1_LOCATION
    + "{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/notify"
)

# fmt: off
notifications_routes = [
    Route(
        URLS_RUNS_NOTIFY,
        notify,
        name="notify",
        methods=["POST"],
    ),
]
