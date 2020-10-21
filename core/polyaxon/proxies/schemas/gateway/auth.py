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

from polyaxon import settings
from polyaxon.api import AUTH_V1_LOCATION
from polyaxon.proxies.schemas.base import get_config
from polyaxon.proxies.schemas.urls import get_service_url, get_ssl_server_name

AUTH_OPTIONS = r"""
    auth_request     {auth_api};
    auth_request_set $auth_status $upstream_status;
"""  # noqa


def get_auth_config():
    return get_config(
        options=AUTH_OPTIONS if settings.PROXIES_CONFIG.auth_enabled else "",
        indent=0,
        auth_api=AUTH_V1_LOCATION,
    )


AUTH_LOCATION_CONFIG = r"""
location = {auth_api} {{
    {resolver}
    {ssl_server_name}
    proxy_pass {service};
    proxy_pass_request_body off;
    proxy_set_header Content-Length "";
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Origin-URI $request_uri;
    proxy_set_header X-Origin-Method $request_method;
    internal;
}}
"""


def get_auth_location_config(resolver: str):
    service = settings.PROXIES_CONFIG.auth_external or get_service_url(
        host=settings.PROXIES_CONFIG.api_host,
        port=settings.PROXIES_CONFIG.api_port,
    )
    if not settings.PROXIES_CONFIG.auth_use_resolver:
        resolver = ""
    return get_config(
        options=AUTH_LOCATION_CONFIG if settings.PROXIES_CONFIG.auth_enabled else "",
        indent=0,
        service=service,
        auth_api=AUTH_V1_LOCATION,
        resolver=resolver,
        ssl_server_name=get_ssl_server_name(service),
    )
