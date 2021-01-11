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
from polyaxon.proxies.schemas.listen import get_listen_config
from polyaxon.proxies.schemas.logging import get_logging_config
from polyaxon.proxies.schemas.timeout import get_timeout_config
from tests.utils import BaseTestCase


@pytest.mark.proxies_mark
class TestBaseSchemas(BaseTestCase):
    SET_PROXIES_SETTINGS = True

    def test_timeout(self):
        expected = """
send_timeout 200;
keepalive_timeout 200;
uwsgi_read_timeout 200;
uwsgi_send_timeout 200;
client_header_timeout 200;
proxy_read_timeout 200;
keepalive_requests 10000;
"""  # noqa
        settings.PROXIES_CONFIG.nginx_timeout = 200
        assert get_timeout_config() == expected

    def test_listen(self):
        expected = """
listen 80;
"""  # noqa
        settings.PROXIES_CONFIG.ssl_enabled = False
        assert get_listen_config(is_proxy=False) == expected

        settings.PROXIES_CONFIG.ssl_enabled = True
        assert get_listen_config(is_proxy=False) == expected

    def test_proxy_listen(self):
        expected = """
listen 80;
"""  # noqa
        settings.PROXIES_CONFIG.ssl_enabled = False
        assert get_listen_config(is_proxy=True) == expected

        expected = """
listen 443 ssl;
ssl on;
"""  # noqa
        settings.PROXIES_CONFIG.ssl_enabled = True
        assert get_listen_config(is_proxy=True) == expected

    def test_logging(self):
        expected = """
error_log /polyaxon/logs/error.log warn;
"""  # noqa
        settings.PROXIES_CONFIG.log_level = "warn"
        assert get_logging_config() == expected
