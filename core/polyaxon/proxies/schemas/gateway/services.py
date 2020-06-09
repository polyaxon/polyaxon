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

PLUGIN_OPTIONS = """
location ~ /{plugin_name}/proxy/([-_.:\w]+)/(.*) {{
    {auth}
    {resolver}
    rewrite_log on;
    rewrite ^/{plugin_name}/proxy/([-_.:\w]+)/(.*) /{plugin_name}/proxy/$1/$2 break;
    proxy_pass http://$1:{port};
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_buffering off;
}}
"""  # noqa


def get_plugin_location_config(name: str, port: int, resolver: str, auth: str):
    return get_config(
        options=PLUGIN_OPTIONS,
        indent=0,
        plugin_name=name,
        port=port,
        resolver=resolver,
        auth=auth,
    )


def get_plugins_location_config(resolver: str, auth: str, proxy_services=None):
    plugins = []

    if proxy_services:
        for plugin, config in proxy_services.items():
            plugins.append(
                get_plugin_location_config(
                    name=plugin, port=config["port"], resolver=resolver, auth=auth
                )
            )

    return plugins


SERVICES_OPTIONS = """
location ~ /services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) {{
    {auth}
    {resolver}
    proxy_pass http://plx-operation-$4.$1.svc.{dns_cluster_with_port};
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}}
"""  # noqa

SERVICES_REWRITE_OPTIONS = """
location ~ /rewrite-services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) {{
    {auth}
    {resolver}
    rewrite_log on;
    rewrite ^/rewrite-services/v1/([-_.:\w]+)/([-_.:\w]+)/([-_.:\w]+)/runs/([-_.:\w]+)/(.*) /$5 break;
    proxy_pass http://plx-operation-$4.$1.svc.{dns_cluster_with_port};
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_hide_header X-Frame-Options;
    proxy_set_header Origin "";
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_buffering off;
}}
"""  # noqa


def get_services_location_config(resolver: str, auth: str, rewrite: bool = False):

    dns_cluster_with_port = settings.PROXIES_CONFIG.dns_custom_cluster
    if settings.PROXIES_CONFIG.services_port != 80:
        dns_cluster_with_port = "{}:{}".format(
            dns_cluster_with_port, settings.PROXIES_CONFIG.services_port
        )
    return get_config(
        options=SERVICES_REWRITE_OPTIONS if rewrite else SERVICES_OPTIONS,
        resolver=resolver,
        auth=auth,
        dns_cluster_with_port=dns_cluster_with_port,
    )
