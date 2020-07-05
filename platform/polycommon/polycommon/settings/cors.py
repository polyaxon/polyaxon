#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

from corsheaders.defaults import default_headers

from polyaxon.services.headers import PolyaxonServiceHeaders
from polycommon.config_manager import ConfigManager


def set_cors(context, config: ConfigManager):
    # session settings
    context["CORS_ALLOW_CREDENTIALS"] = True
    whitelist = config.get_list(
        "POLYAXON_CORS_ORIGIN_WHITELIST", is_optional=True, default=[]
    )
    context["CORS_ORIGIN_WHITELIST"] = whitelist
    context["CORS_ORIGIN_ALLOW_ALL"] = False if whitelist else True

    context["CORS_ALLOW_HEADERS"] = default_headers + (
        PolyaxonServiceHeaders.CLI_VERSION,
        PolyaxonServiceHeaders.CLIENT_VERSION,
        PolyaxonServiceHeaders.INTERNAL,
        PolyaxonServiceHeaders.SERVICE,
    )

    ssl_enabled = config.get_boolean(
        "POLYAXON_SSL_ENABLED", is_optional=True, default=False
    )
    ssl_redirect_enabled = config.get_boolean(
        "POLYAXON_SSL_REDIRECT_ENABLED", is_optional=True, default=False
    )
    context["SSL_ENABLED"] = ssl_enabled
    context["PROTOCOL"] = "http"
    context["WS_PROTOCOL"] = "ws"
    if ssl_enabled:
        context["SESSION_COOKIE_SECURE"] = True
        context["CSRF_COOKIE_SECURE"] = True
        context["SECURE_PROXY_SSL_HEADER"] = ("HTTP_X_FORWARDED_PROTO", "https")
        context["PROTOCOL"] = "https"
        context["WS_PROTOCOL"] = "wss"
    if ssl_redirect_enabled:
        context["SECURE_SSL_REDIRECT"] = True
