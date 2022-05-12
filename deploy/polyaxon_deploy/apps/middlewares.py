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
import json
import os

from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from polyaxon.env_vars.keys import EV_KEYS_CUSTOM_ERRORS_OPTIONS
from polyaxon.plugins.sentry import set_raven_client


def get_middleware(ssl_enabled: bool, disable_cors: bool, gzip: bool):
    errors_options = os.environ.get(EV_KEYS_CUSTOM_ERRORS_OPTIONS)
    if errors_options:
        errors_options = json.loads(errors_options)
    has_raven = set_raven_client(errors_options)

    middleware = []

    if has_raven:  # pragma: nocover
        middleware.append(Middleware(SentryAsgiMiddleware))

    if ssl_enabled:  # pragma: nocover
        middleware.append(Middleware(HTTPSRedirectMiddleware))

    if gzip:
        middleware.append(Middleware(GZipMiddleware, minimum_size=1000))

    if disable_cors:
        middleware.append(
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        )

    return middleware
