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
from polyaxon.api import STREAMS_V1_LOCATION
from polyaxon.proxies.schemas.base import get_config

GUNICORN_OPTIONS = """
location / {{
    proxy_pass http://polyaxon;
    proxy_http_version 1.1;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_intercept_errors {intercept_errors};
}}
"""


def get_gunicorn_config():
    return get_config(options=GUNICORN_OPTIONS, indent=0, intercept_errors="off")


K8S_AUTH_OPTIONS = """
location {app}k8s/auth/ {{
    proxy_method      GET;
    proxy_pass http://polyaxon;
    proxy_http_version 1.1;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Origin-URI $request_uri;
    proxy_intercept_errors {intercept_errors};
}}
"""


def get_k8s_auth_config():
    return get_config(
        options=K8S_AUTH_OPTIONS,
        app=STREAMS_V1_LOCATION,
        indent=0,
        intercept_errors="off",
    )
