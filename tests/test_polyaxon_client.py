# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tempfile

from unittest import TestCase
from mock import patch

from polyaxon.client import settings
from polyaxon.client.config import ClientConfig
from polyaxon.client.client import PolyaxonClient
from polyaxon.client.exceptions import PolyaxonClientException
from polyaxon.client.transport import Transport


class TestPolyaxonClient(TestCase):
    def setUp(self):
        super(TestPolyaxonClient, self).setUp()
        settings.CONTEXT_AUTH_TOKEN_PATH = "{}/{}".format(
            tempfile.mkdtemp(), ".authtoken"
        )

    def test_client_services(self):
        settings.SECRET_USER_TOKEN = None
        with self.assertRaises(PolyaxonClientException):
            PolyaxonClient(host=None, token=None)
        client = PolyaxonClient(host=None, token=None, is_managed=True)
        assert client.host is None
        assert client.http_port == 80
        assert client.ws_port == 80
        assert client.use_https is False
        assert client.token is None

        assert isinstance(client.transport, Transport)
        assert isinstance(client.config, ClientConfig)

        # assert isinstance(client.auth, AuthApi)
        # assert isinstance(client.cluster, ClusterApi)
        # assert isinstance(client.version, VersionApi)
        # assert isinstance(client.project, ProjectApi)
        # assert isinstance(client.experiment, ExperimentApi)
        # assert isinstance(client.user, UserApi)

    def test_from_config(self):
        settings.SECRET_USER_TOKEN = "token"  # noqa
        settings.API_HOST = "localhost"
        client = PolyaxonClient(config=ClientConfig())
        assert client.is_managed is False
        assert client.host == "localhost"
        assert client.http_port == 80
        assert client.ws_port == 80
        assert client.use_https is False
        assert client.token == "token"
        assert client.config.host == "http://localhost:80"

        settings.IS_MANAGED = True
        settings.API_HOST = "api_host"
        client = PolyaxonClient(config=ClientConfig())
        assert client.is_managed is True
        assert client.host == "api_host"
        assert client.http_port == 80
        assert client.ws_port == 80
        assert client.use_https is False
        assert client.token == "token"
        assert client.config.host == "http://api_host:80"

    def test_from_env(self):
        settings.IS_MANAGED = False
        with self.assertRaises(PolyaxonClientException):
            PolyaxonClient()

        settings.SECRET_USER_TOKEN = "token"  # noqa
        settings.API_HOST = "localhost"
        client = PolyaxonClient()
        assert client.is_managed is False
        assert client.host == "localhost"
        assert client.http_port == 80
        assert client.ws_port == 80
        assert client.use_https is False
        assert client.token == "token"
        assert client.config.host == "http://localhost:80"

        settings.IS_MANAGED = True
        settings.API_HOST = "api_host"
        client = PolyaxonClient()
        assert client.is_managed is True
        assert client.host == "api_host"
        assert client.http_port == 80
        assert client.ws_port == 80
        assert client.use_https is False
        assert client.token == "token"
        assert client.config.host == "http://api_host:80"

    @patch("polyaxon.client.client.GlobalConfigManager.get_value")
    @patch("polyaxon.client.client.AuthConfigManager.get_value")
    def test_client(self, get_value_mock1, get_value_mock2):
        get_value_mock1.return_value = "token"
        get_value_mock2.return_value = "host"
        client = PolyaxonClient()

        assert client.host == "host"
        assert client.token == "token"
