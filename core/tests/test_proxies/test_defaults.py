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
from polyaxon.containers.contexts import CONTEXT_ARCHIVE_ROOT
from tests.utils import BaseTestCase


@pytest.mark.proxies_mark
class TestSettings(BaseTestCase):
    SET_PROXIES_SETTINGS = True

    def test_default_values(self):
        assert settings.PROXIES_CONFIG.streams_port == 80
        assert settings.PROXIES_CONFIG.api_port == 80
        assert settings.PROXIES_CONFIG.streams_host == "polyaxon-polyaxon-streams"
        assert settings.PROXIES_CONFIG.api_port == 80
        assert settings.PROXIES_CONFIG.api_host == "polyaxon-polyaxon-api"
        assert settings.PROXIES_CONFIG.services_port == 80
        assert settings.PROXIES_CONFIG.dns_use_resolver is False
        assert settings.PROXIES_CONFIG.dns_custom_cluster == "cluster.local"
        assert settings.PROXIES_CONFIG.dns_backend == "kube-dns"
        assert settings.PROXIES_CONFIG.dns_prefix is None
        assert settings.PROXIES_CONFIG.namespace is None
        assert settings.PROXIES_CONFIG.namespaces is None
        assert settings.PROXIES_CONFIG.log_level == "warn"
        assert settings.PROXIES_CONFIG.nginx_timeout == 650
        assert settings.PROXIES_CONFIG.nginx_indent_char == " "
        assert settings.PROXIES_CONFIG.nginx_indent_width == 4
        assert settings.PROXIES_CONFIG.ssl_path == "/etc/ssl/polyaxon"
        assert settings.PROXIES_CONFIG.ssl_enabled is False
        assert settings.PROXIES_CONFIG.archive_root == CONTEXT_ARCHIVE_ROOT
        assert settings.PROXIES_CONFIG.ssl_path == "/etc/ssl/polyaxon"
        assert settings.PROXIES_CONFIG.ssl_enabled is False
        assert settings.PROXIES_CONFIG.auth_enabled is False
        assert settings.PROXIES_CONFIG.auth_external is None
        assert settings.PROXIES_CONFIG.auth_use_resolver is False
