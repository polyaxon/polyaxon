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
from polyaxon.proxies.schemas.base import get_config

STATIC_LOCATION_OPTIONS = """
location /static/ {{
    alias /polyaxon/static/;
    autoindex on;
    expires                   30d;
    add_header                Cache-Control private;
    gzip_static on;
}}
"""


def get_static_location_config():
    return get_config(options=STATIC_LOCATION_OPTIONS, indent=0)


TMP_LOCATION_OPTIONS = """
location /tmp/ {{
    alias                     /tmp/;
    expires                   0;
    add_header                Cache-Control private;
    internal;
}}
"""


def get_tmp_location_config():
    return get_config(options=TMP_LOCATION_OPTIONS, indent=0)


ARCHIVES_LOCATION_OPTIONS = """
location {archives_root} {{
    alias                     {archives_root};
    expires                   0;
    add_header                Cache-Control private;
    internal;
}}
"""


def get_archives_root_location_config():
    return get_config(
        options=ARCHIVES_LOCATION_OPTIONS,
        indent=0,
        archives_root=settings.PROXIES_CONFIG.archive_root.rstrip("/") + "/",
    )


def get_api_locations_config():
    config = [get_static_location_config(), get_tmp_location_config()]
    return "\n".join(config)


def get_streams_locations_config():
    config = [get_tmp_location_config(), get_archives_root_location_config()]
    return "\n".join(config)
