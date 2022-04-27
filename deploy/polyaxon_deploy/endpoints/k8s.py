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
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from polyaxon import settings
from polyaxon.api import STREAMS_V1_LOCATION
from polyaxon.k8s.async_manager import AsyncK8SManager
from polyaxon.utils.fqn_utils import get_resource_name_for_kind
from polyaxon_deploy.controllers.k8s_check import k8s_check, reverse_k8s
from polyaxon_deploy.controllers.k8s_crd import get_k8s_operation
from polyaxon_deploy.controllers.k8s_pods import get_pods
from polyaxon_deploy.endpoints.base import UJSONResponse


async def k8s_auth(request: Request) -> Response:
    uri = request.headers.get("x-origin-uri")
    if not uri:
        return Response(
            content="This endpoint can only be a sub-requested.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    try:
        path, params = k8s_check(uri)
    except ValueError as e:
        return Response(
            content="Error validating path. {}".format(e),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return await reverse_k8s(path="{}?{}".format(path, params))


async def k8s_inspect(request: Request) -> Response:
    run_uuid = request.path_params["run_uuid"]
    resource_name = get_resource_name_for_kind(run_uuid=run_uuid)
    k8s_manager = AsyncK8SManager(
        namespace=settings.CLIENT_CONFIG.namespace,
        in_cluster=settings.CLIENT_CONFIG.in_cluster,
    )
    await k8s_manager.setup()
    k8s_operation = await get_k8s_operation(
        k8s_manager=k8s_manager, resource_name=resource_name
    )
    data = None
    if k8s_operation:
        data = await get_pods(k8s_manager=k8s_manager, run_uuid=run_uuid)
    if k8s_manager:
        await k8s_manager.close()
    return UJSONResponse(data or {})


URLS_RUNS_K8S_AUTH = STREAMS_V1_LOCATION + "k8s/auth/"
URLS_RUNS_K8S_INSPECT = (
    STREAMS_V1_LOCATION
    + "{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/k8s_inspect"
)

# fmt: off
k8s_routes = [
    Route(
        URLS_RUNS_K8S_AUTH,
        k8s_auth,
        name="k8s",
        methods=["GET"],
    ),
    Route(
        URLS_RUNS_K8S_INSPECT,
        k8s_inspect,
        name="k8s",
        methods=["GET"],
    ),
]
