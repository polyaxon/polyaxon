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

from polyaxon import pkg

VERSION_V1 = "v1"
API_V1 = "api/{}".format(VERSION_V1)
STREAMS_V1 = "streams/{}".format(VERSION_V1)
SERVICES_V1 = "services/{}".format(VERSION_V1)
REWRITE_SERVICES_V1 = "rewrite-services/{}".format(VERSION_V1)
EXTERNAL_V1 = "external/{}".format(VERSION_V1)
REWRITE_EXTERNAL_V1 = "rewrite-external/{}".format(VERSION_V1)
K8S_V1 = "k8s/{}".format(VERSION_V1)
WS_V1 = "ws/{}".format(VERSION_V1)
AUTH_V1 = "auth/{}".format(VERSION_V1)
STATIC_V1 = "static/{}".format(VERSION_V1)
SSO_V1 = "sso"
EVENTS_V1 = "events"
UI_V1 = "ui"
ADMIN_V1 = "_admin"
API_V1_LOCATION = "/" + API_V1 + "/"
STREAMS_V1_LOCATION = "/" + STREAMS_V1 + "/"
UI_V1_LOCATION = "/" + UI_V1 + "/"
STATIC_V1_LOCATION = "/" + STATIC_V1 + "/"
ADMIN_V1_LOCATION = "/" + ADMIN_V1 + "/"
AUTH_V1_LOCATION = "/" + AUTH_V1 + "/"
SSO_V1_LOCATION = "/" + SSO_V1 + "/"
EVENTS_V1_LOCATION = "/" + EVENTS_V1 + "/"
SERVICES_V1_LOCATION = "/" + SERVICES_V1 + "/"
REWRITE_SERVICES_V1_LOCATION = "/" + REWRITE_SERVICES_V1 + "/"
EXTERNAL_V1_LOCATION = "/" + EXTERNAL_V1 + "/"
REWRITE_EXTERNAL_V1_LOCATION = "/" + REWRITE_EXTERNAL_V1 + "/"
K8S_V1_LOCATION = "/" + K8S_V1 + "/"
HEALTHZ_LOCATION = "/healthz/"
POLYAXON_CLOUD_HOST = "https://cloud.polyaxon.com"
LOCALHOST = "http://localhost:8000"
POLYAXON_VERSIONS_HOST = "https://versions.polyaxon.com/?v={}".format(pkg.VERSION)


def get_default_host(host: str = None, service: str = None):
    if host:
        return host
    if service is None:
        return POLYAXON_CLOUD_HOST
    return LOCALHOST
