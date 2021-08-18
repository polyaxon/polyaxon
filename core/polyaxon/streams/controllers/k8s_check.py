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
from typing import List, Tuple
from urllib.parse import urlparse

from starlette import status
from starlette.responses import Response

from polyaxon import settings
from polyaxon.api import K8S_V1_LOCATION
from polyaxon.k8s.async_manager import AsyncK8SManager


def _check_exec(uri_path: List[str], query_params: str):
    pod, container = uri_path
    query_params += "&container={}".format(container)
    path = "api/v1/namespaces/{namespace}/pods/{pod}/exec".format(
        namespace=settings.CLIENT_CONFIG.namespace,
        pod=pod,
    )
    return path, query_params


VALIDATION_PATHS = {
    "k8s_exec": _check_exec,
}


def k8s_check(uri: str) -> Tuple[str, str]:
    parsed_uri = urlparse(uri)
    uri_path = parsed_uri.path.split(K8S_V1_LOCATION)[-1].split("/")
    path_to_check = None
    for vpath in VALIDATION_PATHS:
        if vpath in uri_path:
            path_to_check = vpath
    if not path_to_check:
        raise ValueError("A valid k8s path param is required")
    start = uri_path.index(path_to_check) + 1
    return VALIDATION_PATHS[path_to_check](uri_path[start:], parsed_uri.query)


async def reverse_k8s(path) -> Response:
    if not path:
        return Response(
            content="A valid k8s path param is required",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    config = await AsyncK8SManager.load_config(
        in_cluster=settings.CLIENT_CONFIG.in_cluster
    )
    config_auth = AsyncK8SManager.get_config_auth(config)
    return Response(
        status_code=status.HTTP_200_OK,
        headers={
            "K8S_URI": "{}/{}".format(config.host, path),
            "K8S_TOKEN": config_auth,
        },
    )
