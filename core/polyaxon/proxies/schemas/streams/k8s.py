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

from polyaxon.api import K8S_V1_LOCATION, STREAMS_V1_LOCATION
from polyaxon.proxies.schemas.base import get_config

AUTH_OPTIONS = r"""
    auth_request     {auth_api};
    auth_request_set $auth_status $upstream_status;
"""  # noqa


def get_auth_config():
    return get_config(
        options=AUTH_OPTIONS,
        indent=0,
        auth_api=STREAMS_V1_LOCATION,
    )


K8S_LOCATION_OPTIONS = r"""
location {app} {{
    auth_request     {streams_api}k8s/auth/;
    auth_request_set $auth_status $upstream_status;
    auth_request_set $k8s_token $upstream_http_k8s_token;
    auth_request_set $k8s_uri $upstream_http_k8s_uri;
    proxy_pass $k8s_uri;
    proxy_http_version 1.1;
    proxy_redirect     off;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Authorization "bearer $k8s_token";
    proxy_buffering off;
}}
"""  # noqa


def get_k8s_root_location_config():
    return get_config(
        options=K8S_LOCATION_OPTIONS,
        app=K8S_V1_LOCATION,
        streams_api=STREAMS_V1_LOCATION,
    )
