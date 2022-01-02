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
import json
import os

from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.routing import Route

from polyaxon import settings
from polyaxon.api import STREAMS_V1
from polyaxon.env_vars.keys import POLYAXON_KEYS_CUSTOM_ERRORS_OPTIONS
from polyaxon.plugins.sentry import set_raven_client
from polyaxon.streams.app import endpoints
from polyaxon.streams.app.fs import AppFS

errors_options = os.environ.get(POLYAXON_KEYS_CUSTOM_ERRORS_OPTIONS)
if errors_options:
    errors_options = json.loads(errors_options)
has_raven = set_raven_client(errors_options)

STREAMS_URL = "/{}".format(STREAMS_V1)
URLS_RUNS_INTERNAL_LOGS = (
    STREAMS_URL
    + "/{namespace:str}"
    + "/_internal"
    + "/{owner:str}/{project:str}/runs/{run_uuid:str}/{run_kind:str}/logs"
)
URLS_RUNS_LOGS = (
    STREAMS_URL + "/{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/logs"
)
URLS_RUNS_K8S_AUTH = STREAMS_URL + "/k8s/auth/"
URLS_RUNS_K8S_INSPECT = (
    STREAMS_URL
    + "/{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/k8s_inspect"
)
URLS_RUNS_MULTI_EVENTS = (
    STREAMS_URL
    + "/{namespace:str}/{owner:str}/{project:str}/runs/multi/events/{event_kind:str}"
)
URLS_RUNS_EVENTS = (
    STREAMS_URL + "/{namespace:str}/{owner:str}/{project:str}/runs/"
    "{run_uuid:str}/events/{event_kind:str}"
)
URLS_RUNS_RESOURCES = (
    STREAMS_URL + "/{namespace:str}/{owner:str}/{project:str}/runs/"
    "{run_uuid:str}/resources"
)
URLS_RUNS_NOTIFY = (
    STREAMS_URL
    + "/{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/notify"
)
URLS_RUNS_ARTIFACT = (
    STREAMS_URL
    + "/{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/artifact"
)
URLS_RUNS_EMBEDDED_ARTIFACT = (
    STREAMS_URL
    + "/{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/embedded_artifact"
)
URLS_RUNS_RO_ARTIFACT = (
    STREAMS_URL
    + "/{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/ro_artifact/{path:path}"
)
URLS_RUNS_ARTIFACTS = (
    STREAMS_URL
    + "/{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/artifacts"
)
URLS_RUNS_ARTIFACTS_TREE = (
    STREAMS_URL
    + "/{namespace:str}/{owner:str}/{project:str}/runs/{run_uuid:str}/artifacts/tree"
)

# fmt: off
routes = [
    Route(
        URLS_RUNS_INTERNAL_LOGS, endpoints.collect_logs,
        name="logs",
        methods=["POST"]
    ),
    Route(
        URLS_RUNS_MULTI_EVENTS, endpoints.get_multi_run_events,
        name="multi_run_events",
        methods=["GET"]
    ),
    Route(
        URLS_RUNS_LOGS, endpoints.get_logs,
        name="logs",
        methods=["GET"]
    ),
    Route(
        URLS_RUNS_K8S_AUTH, endpoints.k8s_auth,
        name="k8s",
        methods=["GET"]
    ),
    Route(
        URLS_RUNS_K8S_INSPECT, endpoints.k8s_inspect,
        name="k8s",
        methods=["GET"]
    ),
    Route(
        URLS_RUNS_RESOURCES, endpoints.get_run_resources,
        name="resources",
        methods=["GET"]
    ),
    Route(
        URLS_RUNS_NOTIFY, endpoints.notify,
        name="notify",
        methods=["POST"]
    ),
    Route(
        URLS_RUNS_ARTIFACT, endpoints.handle_artifact,
        name="download_artifact",
        methods=["GET", "DELETE", "POST"]
    ),
    Route(
        URLS_RUNS_EMBEDDED_ARTIFACT, endpoints.handle_artifact,
        name="download_embedded_artifact",
        methods=["GET"]
    ),
    Route(
        URLS_RUNS_RO_ARTIFACT, endpoints.ro_artifact,
        name="read_only_artifact",
        methods=["GET"]
    ),
    Route(
        URLS_RUNS_ARTIFACTS, endpoints.handle_artifacts,
        name="download_artifacts",
        methods=["GET", "DELETE", "POST"]
    ),
    Route(
        URLS_RUNS_ARTIFACTS_TREE, endpoints.tree_artifacts,
        name="list_artifacts",
        methods=["GET"]
    ),
    Route(
        URLS_RUNS_EVENTS, endpoints.get_run_events,
        name="events",
        methods=["GET"]
    ),
    Route("/500", endpoints.error),
    Route("/healthz", endpoints.health),
]

middleware = []

if has_raven:  # pragma: nocover
    middleware += [Middleware(SentryAsgiMiddleware)]

if settings.CLIENT_CONFIG.verify_ssl:  # pragma: nocover
    middleware += [Middleware(HTTPSRedirectMiddleware)]

exception_handlers = {
    404: endpoints.not_found,
    500: endpoints.server_error,
}

app = Starlette(
    debug=settings.CLIENT_CONFIG.debug,
    routes=routes,
    middleware=middleware,
    exception_handlers=exception_handlers,
    on_startup=[AppFS.set_fs],
    on_shutdown=[AppFS.close_fs],
)
