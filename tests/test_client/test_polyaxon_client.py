# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tempfile

from unittest import TestCase

import polyaxon_sdk

from polyaxon import settings
from polyaxon.client.client import PolyaxonClient
from polyaxon.client.transport import Transport
from polyaxon.schemas.cli.client_configuration import ClientConfig


class TestPolyaxonClient(TestCase):
    def setUp(self):
        super(TestPolyaxonClient, self).setUp()
        settings.CONTEXT_AUTH_TOKEN_PATH = "{}/{}".format(
            tempfile.mkdtemp(), ".polyaxonauth"
        )

    def test_client_services(self):
        client = PolyaxonClient(token=None)
        assert client.config.token is None

        assert isinstance(client.transport, Transport)
        assert isinstance(client.config, ClientConfig)

        assert isinstance(client.auth_v1, polyaxon_sdk.AuthV1Api)
        assert isinstance(client.versions_v1, polyaxon_sdk.VersionsV1Api)
        assert isinstance(client.projects_v1, polyaxon_sdk.ProjectsV1Api)
        assert isinstance(client.runs_v1, polyaxon_sdk.RunsV1Api)
        assert isinstance(client.users_v1, polyaxon_sdk.UsersV1Api)

    def test_from_config(self):
        settings.config.host = "localhost"
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
