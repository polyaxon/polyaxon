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
from polyaxon.proxies.schemas.api.uwsgi import get_uwsgi_config
from polyaxon.proxies.schemas.buffering import get_buffering_config
from polyaxon.proxies.schemas.charset import get_charset_config
from polyaxon.proxies.schemas.error_page import get_error_page_config
from polyaxon.proxies.schemas.gzip import get_gzip_config
from polyaxon.proxies.schemas.listen import get_listen_config
from polyaxon.proxies.schemas.locations import get_api_locations_config
from polyaxon.proxies.schemas.logging import get_logging_config
from polyaxon.proxies.schemas.timeout import get_timeout_config


def get_base_config():
    config = [get_listen_config(is_proxy=False, port=settings.PROXIES_CONFIG.api_port)]
    config += [
        get_logging_config(),
        get_gzip_config(),
        get_charset_config(),
        get_buffering_config(),
        get_timeout_config(),
        get_uwsgi_config(),
        get_error_page_config(),
        get_api_locations_config(),
    ]

    return "\n".join(config)
