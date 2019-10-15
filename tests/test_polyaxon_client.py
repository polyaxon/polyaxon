# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tempfile

from unittest import TestCase

from polyaxon.client import settings
from polyaxon.client.api.auth import AuthApi
from polyaxon.client.api.bookmark import BookmarkApi
from polyaxon.client.api.cluster import ClusterApi
from polyaxon.client.api.experiment import ExperimentApi
from polyaxon.client.api.project import ProjectApi
from polyaxon.client.api.user import UserApi
from polyaxon.client.api.version import VersionApi
from polyaxon.client.api_config import ApiConfig
from polyaxon.client.client import PolyaxonClient
from polyaxon.client.exceptions import PolyaxonClientException
from polyaxon.client.transport import Transport


class TestPolyaxonClient(TestCase):
    def setUp(self):
        super(TestPolyaxonClient, self).setUp()
        settings.CONTEXT_AUTH_TOKEN_PATH = "{}/{}".format(
            tempfile.mkdtemp(), ".authtoken"
        )

    def test_client(self):
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
        assert isinstance(client.api_config, ApiConfig)

        assert isinstance(client.auth, AuthApi)
        assert isinstance(client.cluster, ClusterApi)
        assert isinstance(client.version, VersionApi)
        assert isinstance(client.project, ProjectApi)
        assert isinstance(client.experiment, ExperimentApi)
        assert isinstance(client.bookmark, BookmarkApi)
        assert isinstance(client.user, UserApi)

    def test_from_config(self):
        settings.SECRET_USER_TOKEN = "token"  # noqa
        settings.API_HOST = "localhost"
        client = PolyaxonClient(api_config=ApiConfig())
        assert client.is_managed is False
        assert client.host == "localhost"
        assert client.http_port == 80
        assert client.ws_port == 80
        assert client.use_https is False
        assert client.token == "token"
        assert client.api_config.http_host == "http://localhost:80"
        assert client.api_config.ws_host == "ws://localhost:80"

        settings.IS_MANAGED = True
        settings.API_HOST = "api_host"
        client = PolyaxonClient(api_config=ApiConfig())
        assert client.is_managed is True
        assert client.host == "api_host"
        assert client.http_port == 80
        assert client.ws_port == 80
        assert client.use_https is False
        assert client.token == "token"
        assert client.api_config.http_host == "http://api_host:80"
        assert client.api_config.ws_host == "ws://api_host:80"

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
        assert client.api_config.http_host == "http://localhost:80"
        assert client.api_config.ws_host == "ws://localhost:80"

        settings.IS_MANAGED = True
        settings.API_HOST = "api_host"
        client = PolyaxonClient()
        assert client.is_managed is True
        assert client.host == "api_host"
        assert client.http_port == 80
        assert client.ws_port == 80
        assert client.use_https is False
        assert client.token == "token"
        assert client.api_config.http_host == "http://api_host:80"
        assert client.api_config.ws_host == "ws://api_host:80"
