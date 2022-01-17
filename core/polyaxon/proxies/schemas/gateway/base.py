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
from polyaxon.proxies.schemas.base import clean_config
from polyaxon.proxies.schemas.buffering import get_buffering_config
from polyaxon.proxies.schemas.charset import get_charset_config
from polyaxon.proxies.schemas.error_page import get_error_page_config
from polyaxon.proxies.schemas.favicon import get_favicon_config
from polyaxon.proxies.schemas.gateway.api import get_api_location_config
from polyaxon.proxies.schemas.gateway.auth import (
    get_auth_config,
    get_auth_location_config,
)
from polyaxon.proxies.schemas.gateway.dns import get_resolver
from polyaxon.proxies.schemas.gateway.healthz import get_healthz_location_config
from polyaxon.proxies.schemas.gateway.services import get_services_location_config
from polyaxon.proxies.schemas.gateway.ssl import get_ssl_config
from polyaxon.proxies.schemas.gateway.streams import (
    get_k8s_location_config,
    get_streams_location_config,
)
from polyaxon.proxies.schemas.gzip import get_gzip_config
from polyaxon.proxies.schemas.listen import get_listen_config
from polyaxon.proxies.schemas.logging import get_logging_config
from polyaxon.proxies.schemas.robots import get_robots_config
from polyaxon.proxies.schemas.timeout import get_timeout_config


def get_base_config():
    resolver = get_resolver()
    auth = get_auth_config()
    config = [
        get_listen_config(
            is_proxy=True, port=settings.PROXIES_CONFIG.gateway_target_port
        )
    ]
    if settings.PROXIES_CONFIG.ssl_enabled:
        config.append(get_ssl_config())
    config += [
        get_logging_config(),
        get_gzip_config(),
        get_charset_config(),
        get_buffering_config(),
        get_timeout_config(),
        get_error_page_config(),
        get_robots_config(),
        get_favicon_config(),
        get_healthz_location_config(),
        get_auth_location_config(resolver=resolver),
        get_streams_location_config(resolver=resolver, auth=auth),
        get_k8s_location_config(resolver=resolver, auth=auth),
        get_services_location_config(
            resolver=resolver, auth=auth, rewrite=False, external=False
        ),
        get_services_location_config(
            resolver=resolver, auth=auth, rewrite=True, external=False
        ),
        get_services_location_config(
            resolver=resolver, auth=auth, rewrite=False, external=True
        ),
        get_services_location_config(
            resolver=resolver, auth=auth, rewrite=True, external=True
        ),
        get_api_location_config(resolver=resolver, auth=auth),
    ]
    # config += get_plugins_location_config(resolver=resolver, auth=auth)

    return clean_config(config)
