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
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from polyaxon import settings
from polyaxon.env_vars.keys import POLYAXON_KEYS_CUSTOM_ERRORS_OPTIONS
from polyaxon.plugins.sentry import set_raven_client

errors_options = os.environ.get(POLYAXON_KEYS_CUSTOM_ERRORS_OPTIONS)
if errors_options:
    errors_options = json.loads(errors_options)
has_raven = set_raven_client(errors_options)

middleware = []

if has_raven:  # pragma: nocover
    middleware += [Middleware(SentryAsgiMiddleware)]

if settings.CLIENT_CONFIG.verify_ssl:  # pragma: nocover
    middleware += [Middleware(HTTPSRedirectMiddleware)]
