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
import pytest

from polyaxon import settings
from polyaxon.proxies.schemas.gateway.forward import get_forward_cmd
from tests.utils import BaseTestCase


@pytest.mark.proxies_mark
class TestGatewayForward(BaseTestCase):
    SET_PROXIES_SETTINGS = True

    def test_forward_config_empty(self):
        assert get_forward_cmd() is None

    def test_forward_config_wrong(self):
        settings.PROXIES_CONFIG.forward_proxy_kind = "foo"
        settings.PROXIES_CONFIG.has_forward_proxy = True
        settings.PROXIES_CONFIG.forward_proxy_port = 8080
        settings.PROXIES_CONFIG.forward_proxy_host = "123.123.123.123"
        settings.PROXIES_CONFIG.api_port = 443
        settings.PROXIES_CONFIG.api_host = "cloud.polyaxon.com"
        assert get_forward_cmd() is None

    def test_forward_config_transparent(self):
        settings.PROXIES_CONFIG.forward_proxy_kind = "transparent"
        settings.PROXIES_CONFIG.has_forward_proxy = True
        settings.PROXIES_CONFIG.forward_proxy_port = 8080
        settings.PROXIES_CONFIG.forward_proxy_host = "123.123.123.123"
        expected = """
#!/bin/bash
set -e
set -o pipefail

socat TCP4-LISTEN:8443,reuseaddr,fork TCP:123.123.123.123:8080
"""  # noqa
        assert get_forward_cmd() == expected

    def test_forward_config_connect(self):
        settings.PROXIES_CONFIG.forward_proxy_kind = "connect"
        settings.PROXIES_CONFIG.has_forward_proxy = True
        settings.PROXIES_CONFIG.forward_proxy_port = 8080
        settings.PROXIES_CONFIG.forward_proxy_host = "123.123.123.123"
        settings.PROXIES_CONFIG.api_port = 443
        settings.PROXIES_CONFIG.api_host = "cloud.polyaxon.com"
        expected = """
#!/bin/bash
set -e
set -o pipefail

socat TCP4-LISTEN:8443,reuseaddr,fork,bind=127.0.0.1 PROXY:123.123.123.123:cloud.polyaxon.com:443,proxyport=8080
"""  # noqa
        assert get_forward_cmd() == expected

    def test_forward_config_default(self):
        settings.PROXIES_CONFIG.has_forward_proxy = True
        settings.PROXIES_CONFIG.forward_proxy_port = 8080
        settings.PROXIES_CONFIG.forward_proxy_host = "123.123.123.123"
        settings.PROXIES_CONFIG.api_port = 443
        settings.PROXIES_CONFIG.api_host = "cloud.polyaxon.com"
        expected = """
#!/bin/bash
set -e
set -o pipefail

socat TCP4-LISTEN:8443,reuseaddr,fork,bind=127.0.0.1 PROXY:123.123.123.123:cloud.polyaxon.com:443,proxyport=8080
"""  # noqa
        assert get_forward_cmd() == expected
