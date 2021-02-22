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
import tempfile

import polyaxon_sdk

from polyaxon import settings
from polyaxon.client.client import PolyaxonClient
from polyaxon.schemas.cli.client_config import ClientConfig
from tests.utils import BaseTestCase


@pytest.mark.client_mark
class TestPolyaxonClient(BaseTestCase):
    def setUp(self):
        super().setUp()
        settings.CONTEXT_AUTH_TOKEN_PATH = "{}/{}".format(tempfile.mkdtemp(), ".auth")

    def test_client_services(self):
        settings.AUTH_CONFIG.token = None
        client = PolyaxonClient(token=None)
        assert client.config.token is None

        assert isinstance(client.config, ClientConfig)

        assert isinstance(client.auth_v1, polyaxon_sdk.AuthV1Api)
        assert isinstance(client.versions_v1, polyaxon_sdk.VersionsV1Api)
        assert isinstance(client.projects_v1, polyaxon_sdk.ProjectsV1Api)
        assert isinstance(client.runs_v1, polyaxon_sdk.RunsV1Api)
        assert isinstance(client.users_v1, polyaxon_sdk.UsersV1Api)

    def test_from_config(self):
        settings.CLIENT_CONFIG.host = "localhost"
        client = PolyaxonClient(config=ClientConfig())
        assert client.config.is_managed is False
        assert client.config.host == "https://cloud.polyaxon.com"
        assert client.config.token is None

    def test_from_settings(self):
        settings.CLIENT_CONFIG.is_managed = True
        settings.CLIENT_CONFIG.host = "api_host"
        client = PolyaxonClient(token="token")
        assert client.config.is_managed is True
        assert client.config.host == "api_host"
        assert client.config.token == "token"
        assert client.config.base_url == "api_host/api/v1"
