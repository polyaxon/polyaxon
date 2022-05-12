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

from typing import Any

import ujson

from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route


async def health(request: Request) -> Response:
    return Response(status_code=status.HTTP_200_OK)


async def error(request: Request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


async def not_found(request: Request, exc) -> Response:
    """
    Return an HTTP 404 page.
    """
    return Response(status_code=status.HTTP_404_NOT_FOUND)


async def server_error(request: Request, exc):
    """
    Return an HTTP 500 page.
    """
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return ujson.dumps(content, ensure_ascii=False).encode("utf-8")


class ConfigResponse(JSONResponse):
    def render(self, content: Any, is_serialized: bool = True) -> bytes:
        return content.encode("utf-8")


base_routes = [
    Route("/500", error),
    Route("/healthz", health),
]

exception_handlers = {
    404: not_found,
    500: server_error,
}
