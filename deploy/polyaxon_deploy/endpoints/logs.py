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
from starlette.datastructures import QueryParams
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from polyaxon import settings
from polyaxon.api import STREAMS_V1_LOCATION
from polyaxon.k8s.async_manager import AsyncK8SManager
from polyaxon.k8s.logging.async_monitor import query_k8s_operation_logs
from polyaxon.utils.bool_utils import to_bool
from polyaxon.utils.date_utils import parse_datetime
from polyaxon.utils.fqn_utils import get_resource_name, get_resource_name_for_kind
from polyaxon.utils.serialization import datetime_serialize
from polyaxon_deploy.connections.fs import AppFS
from polyaxon_deploy.controllers.k8s_crd import get_k8s_operation
from polyaxon_deploy.controllers.logs import (
    get_archived_operation_logs,
    get_operation_logs,
    get_tmp_operation_logs,
)
from polyaxon_deploy.endpoints.base import UJSONResponse
from polyaxon_deploy.logger import logger
from polyaxon_deploy.tasks.logs import clean_tmp_logs, upload_logs


async def get_logs(request: Request) -> UJSONResponse:
    run_uuid = request.path_params["run_uuid"]
    force = to_bool(request.query_params.get("force"), handle_none=True)
    last_time = QueryParams(request.url.query).get("last_time")
    if last_time:
        last_time = parse_datetime(last_time).astimezone()
    last_file = QueryParams(request.url.query).get("last_file")
    files = []

    if last_time:
        resource_name = get_resource_name(run_uuid=run_uuid)

        k8s_manager = AsyncK8SManager(
            namespace=settings.CLIENT_CONFIG.namespace,
            in_cluster=settings.CLIENT_CONFIG.in_cluster,
        )
        await k8s_manager.setup()
        k8s_operation = await get_k8s_operation(
            k8s_manager=k8s_manager, resource_name=resource_name
        )
        if k8s_operation:
            operation_logs, last_time = await get_operation_logs(
                k8s_manager=k8s_manager,
                k8s_operation=k8s_operation,
                instance=run_uuid,
                last_time=last_time,
            )
        else:
            operation_logs, last_time = await get_tmp_operation_logs(
                fs=await AppFS.get_fs(), run_uuid=run_uuid, last_time=last_time
            )
        if k8s_manager:
            await k8s_manager.close()

    else:
        operation_logs, last_file, files = await get_archived_operation_logs(
            fs=await AppFS.get_fs(),
            run_uuid=run_uuid,
            last_file=last_file,
            check_cache=not force,
        )
    response = dict(
        last_time=datetime_serialize("last_time", {"last_time": last_time}),
        last_file=last_file,
        logs=operation_logs,
        files=files,
    )
    return UJSONResponse(response)


async def collect_logs(request: Request) -> Response:
    run_uuid = request.path_params["run_uuid"]
    run_kind = request.path_params["run_kind"]
    resource_name = get_resource_name_for_kind(run_uuid=run_uuid, run_kind=run_kind)
    k8s_manager = AsyncK8SManager(
        namespace=settings.CLIENT_CONFIG.namespace,
        in_cluster=settings.CLIENT_CONFIG.in_cluster,
    )
    await k8s_manager.setup()
    k8s_operation = await get_k8s_operation(
        k8s_manager=k8s_manager, resource_name=resource_name
    )
    if not k8s_operation:
        errors = "Run's logs was not collected, resource was not found."
        logger.warning(errors)
        return UJSONResponse(
            content={"errors": errors},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    operation_logs, _ = await query_k8s_operation_logs(
        instance=run_uuid, k8s_manager=k8s_manager, last_time=None
    )
    if k8s_manager:
        await k8s_manager.close()
    if not operation_logs:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    try:
        await upload_logs(
            fs=await AppFS.get_fs(), run_uuid=run_uuid, logs=operation_logs
        )
    except Exception as e:
        errors = (
            "Run's logs was not collected, an error was raised while uploading the data %s."
            % e
        )
        logger.warning(errors)
        return UJSONResponse(
            content={"errors": errors},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if settings.AGENT_CONFIG.is_replica:
        task = BackgroundTask(clean_tmp_logs, run_uuid=run_uuid)
        return Response(background=task)
    return Response(status_code=status.HTTP_200_OK)


URLS_RUNS_INTERNAL_LOGS = (
    STREAMS_V1_LOCATION
    + "{namespace:str}"
    + "/_internal"
    + "/{owner:str}/{project:str}/runs/{run_uuid:str}/{run_kind:str}/logs"
)
URLS_RUNS_LOGS = (
    STREAMS_V1_LOCATION
    + "{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/logs"
)


# fmt: off
logs_routes = [
    Route(
        URLS_RUNS_INTERNAL_LOGS,
        collect_logs,
        name="logs",
        methods=["POST"],
    ),
    Route(
        URLS_RUNS_LOGS,
        get_logs,
        name="logs",
        methods=["GET"],
    ),
]
