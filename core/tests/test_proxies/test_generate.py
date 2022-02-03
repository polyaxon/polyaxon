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

import os
import pytest
import tempfile

from polyaxon import settings
from polyaxon.proxies.generators import (
    generate_api_conf,
    generate_forward_proxy_cmd,
    generate_gateway_conf,
    generate_streams_conf,
)
from polyaxon.utils.test_utils import BaseTestCase


@pytest.mark.proxies_mark
class TestGenerate(BaseTestCase):
    SET_PROXIES_SETTINGS = True

    def test_generate_api_conf(self):
        tmp_dir = tempfile.mkdtemp()
        assert os.listdir(tmp_dir) == []
        generate_api_conf(path=tmp_dir)
        assert set(os.listdir(tmp_dir)) == {"polyaxon.main.conf", "polyaxon.base.conf"}

    def test_generate_gateway_conf(self):
        tmp_dir = tempfile.mkdtemp()
        assert os.listdir(tmp_dir) == []
        generate_gateway_conf(path=tmp_dir)
        assert set(os.listdir(tmp_dir)) == {
            "polyaxon.main.conf",
            "polyaxon.base.conf",
            "polyaxon.redirect.conf",
        }

    def test_generate_forward_proxy_conf(self):
        tmp_dir = tempfile.mkdtemp()
        assert os.listdir(tmp_dir) == []
        generate_forward_proxy_cmd(path=tmp_dir)
        assert os.listdir(tmp_dir) == []

        settings.PROXIES_CONFIG.has_forward_proxy = True
        settings.PROXIES_CONFIG.forward_proxy_port = 443
        settings.PROXIES_CONFIG.forward_proxy_host = "123.123.123.123"
        generate_forward_proxy_cmd(path=tmp_dir)
        assert os.listdir(tmp_dir) == ["forward_proxy.sh"]

    def test_generate_forward_proxy_conf_valid_kind(self):
        tmp_dir = tempfile.mkdtemp()
        assert os.listdir(tmp_dir) == []
        settings.PROXIES_CONFIG.forward_proxy_kind = "connect"
        generate_forward_proxy_cmd(path=tmp_dir)
        assert os.listdir(tmp_dir) == []

        settings.PROXIES_CONFIG.has_forward_proxy = True
        settings.PROXIES_CONFIG.forward_proxy_port = 443
        settings.PROXIES_CONFIG.forward_proxy_host = "123.123.123.123"
        generate_forward_proxy_cmd(path=tmp_dir)
        assert os.listdir(tmp_dir) == ["forward_proxy.sh"]

    def test_generate_forward_proxy_conf_wrong_kind(self):
        tmp_dir = tempfile.mkdtemp()
        assert os.listdir(tmp_dir) == []
        settings.PROXIES_CONFIG.forward_proxy_kind = "foo"
        generate_forward_proxy_cmd(path=tmp_dir)
        assert os.listdir(tmp_dir) == []

        settings.PROXIES_CONFIG.has_forward_proxy = True
        settings.PROXIES_CONFIG.forward_proxy_port = 443
        settings.PROXIES_CONFIG.forward_proxy_host = "123.123.123.123"
        generate_forward_proxy_cmd(path=tmp_dir)
        assert os.listdir(tmp_dir) == []

    def test_generate_streams_conf(self):
        tmp_dir = tempfile.mkdtemp()
        assert os.listdir(tmp_dir) == []
        generate_streams_conf(path=tmp_dir)
        assert set(os.listdir(tmp_dir)) == {"polyaxon.main.conf", "polyaxon.base.conf"}
