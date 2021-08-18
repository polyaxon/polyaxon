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

from polyaxon import settings
from polyaxon.proxies.schemas.base import get_config
from polyaxon.proxies.schemas.urls import get_service_url

STREAMS_OPTIONS = r"""
location /streams/ {{
    {auth}
    {resolver}
    proxy_pass {service};
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}}
"""  # noqa


def get_streams_location_config(resolver: str, auth: str):
    service = get_service_url(
        host=settings.PROXIES_CONFIG.streams_host,
        port=settings.PROXIES_CONFIG.streams_port,
    )
    return get_config(
        options=STREAMS_OPTIONS, resolver=resolver, auth=auth, service=service
    )


K8S_OPTIONS = r"""
location /k8s/ {{
    {auth}
    {resolver}
    proxy_pass {service};
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}}
"""  # noqa


def get_k8s_location_config(resolver: str, auth: str):
    service = get_service_url(
        host=settings.PROXIES_CONFIG.streams_host,
        port=settings.PROXIES_CONFIG.streams_port,
    )
    return get_config(
        options=K8S_OPTIONS, resolver=resolver, auth=auth, service=service
    )
