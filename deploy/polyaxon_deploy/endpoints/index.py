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
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from polyaxon import dist
from polyaxon.api import API_V1_LOCATION
from polyaxon.env_vars.keys import EV_KEYS_STATIC_ROOT
from polyaxon_deploy import pkg
from polyaxon_deploy.endpoints.base import UJSONResponse

static_root = os.environ.get(EV_KEYS_STATIC_ROOT, os.path.dirname(__file__))
templates_path = os.path.join(static_root, "templates")

templates = Jinja2Templates(directory=templates_path)


async def homepage(request):
    return templates.TemplateResponse("sandbox/index.html", {"request": request})


async def installation(request: Request):
    from polyaxon.cli.session import get_installation_key

    key = get_installation_key(None)
    data = {
        "key": key,
        "version": pkg.VERSION,
        "dist": dist.SANDBOX,
    }
    return UJSONResponse(data)


class GzipStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if "gz" in path:
            response._headers["content-encoding"] = "gzip"
        return response


home_routes = [
    Route(API_V1_LOCATION + "installation", installation),
    Mount("/static", GzipStaticFiles(directory=static_root), name="static"),
    Route("/", endpoint=homepage),
    Route("/ui/{any:path}", endpoint=homepage),
]
