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

from starlette.applications import Starlette

from polyaxon import settings
from polyaxon_deploy.apps.middlewares import get_middleware
from polyaxon_deploy.connections.fs import AppFS
from polyaxon_deploy.endpoints.artifacts import artifacts_routes
from polyaxon_deploy.endpoints.base import base_routes, exception_handlers
from polyaxon_deploy.endpoints.events import events_routes
from polyaxon_deploy.endpoints.k8s import k8s_routes
from polyaxon_deploy.endpoints.logs import logs_routes
from polyaxon_deploy.endpoints.notifications import notifications_routes

routes = (
    logs_routes
    + k8s_routes
    + notifications_routes
    + artifacts_routes
    + events_routes
    + base_routes
)

app = Starlette(
    debug=settings.CLIENT_CONFIG.debug,
    routes=routes,
    middleware=get_middleware(
        ssl_enabled=settings.CLIENT_CONFIG.verify_ssl,
        disable_cors=False,
        gzip=True,
    ),
    exception_handlers=exception_handlers,
    on_startup=[AppFS.set_fs],
    on_shutdown=[AppFS.close_fs],
)
