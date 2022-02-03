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

OPTIONS = r"""
#!/bin/bash
set -e
set -o pipefail

{cmd}
"""


def get_forward_cmd():
    if not settings.PROXIES_CONFIG.has_forward_proxy:
        return

    cmd = None
    if settings.PROXIES_CONFIG.forward_proxy_kind == "transparent":
        cmd = "socat TCP4-LISTEN:8443,reuseaddr,fork TCP:{proxy_host}:{proxy_port}".format(
            proxy_host=settings.PROXIES_CONFIG.forward_proxy_host,
            proxy_port=settings.PROXIES_CONFIG.forward_proxy_port,
        )
    elif (
        settings.PROXIES_CONFIG.forward_proxy_kind is None
        or settings.PROXIES_CONFIG.forward_proxy_kind == "connect"
    ):
        cmd = (
            "socat TCP4-LISTEN:8443,reuseaddr,fork,bind=127.0.0.1 "
            "PROXY:{proxy_host}:{api_host}:{api_port},proxyport={proxy_port}".format(
                api_host=settings.PROXIES_CONFIG.api_host,
                api_port=settings.PROXIES_CONFIG.api_port,
                proxy_host=settings.PROXIES_CONFIG.forward_proxy_host,
                proxy_port=settings.PROXIES_CONFIG.forward_proxy_port,
            )
        )

    if not cmd:
        return

    return get_config(
        options=OPTIONS,
        indent=0,
        cmd=cmd,
    )
