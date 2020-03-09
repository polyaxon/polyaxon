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

from tests.utils import BaseTestCase

from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_API_HOST,
    POLYAXON_KEYS_DEBUG,
    POLYAXON_KEYS_VERIFY_SSL,
)
from polyaxon.schemas.cli.client_config import ClientConfig


class TestClientConfig(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.host = "http://localhost:8000"
        self.config = ClientConfig(host=self.host, version="v1", token="token")

    def test_client_config(self):
        config_dict = {
            POLYAXON_KEYS_DEBUG: True,
            POLYAXON_KEYS_API_HOST: "http://localhost:8000",
            POLYAXON_KEYS_VERIFY_SSL: True,
        }
        config = ClientConfig.from_dict(config_dict)
        assert config.debug is True
        assert config.host == "http://localhost:8000"
        assert config.base_url == "http://localhost:8000/api/v1"
        assert config.verify_ssl is True

    def test_base_urls(self):
        assert self.config.base_url == "{}/api/v1".format(self.host)

    def test_is_managed(self):
        config = ClientConfig(host=None, is_managed=True)
        assert config.is_managed is True
        assert config.version == "v1"
        assert config.host == "https://cloud.polyaxon.com"
