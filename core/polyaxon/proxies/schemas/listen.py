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

HTTP_OPTIONS = """
listen {port};
"""

SSL_OPTIONS = """
listen 443 ssl;
ssl on;
"""


def get_listen_config(is_proxy: bool, port=8000) -> str:
    options = (
        SSL_OPTIONS
        if is_proxy and settings.PROXIES_CONFIG.ssl_enabled
        else HTTP_OPTIONS
    )
    return get_config(options=options, indent=0, port=port)
