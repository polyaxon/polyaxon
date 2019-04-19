# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tempfile

from unittest import TestCase

from polyaxon_client import settings
from polyaxon_client.api.auth import AuthApi
from polyaxon_client.api.bookmark import BookmarkApi
from polyaxon_client.api.build_job import BuildJobApi
from polyaxon_client.api.cluster import ClusterApi
from polyaxon_client.api.experiment import ExperimentApi
from polyaxon_client.api.experiment_group import ExperimentGroupApi
from polyaxon_client.api.experiment_job import ExperimentJobApi
from polyaxon_client.api.job import JobApi
from polyaxon_client.api.project import ProjectApi
from polyaxon_client.api.user import UserApi
from polyaxon_client.api.version import VersionApi
from polyaxon_client.api_config import ApiConfig
from polyaxon_client.client import PolyaxonClient
from polyaxon_client.exceptions import PolyaxonClientException
from polyaxon_client.transport import Transport


class TestPolyaxonClient(TestCase):

    def setUp(self):
        super(TestPolyaxonClient, self).setUp()
        settings.CONTEXT_AUTH_TOKEN_PATH = '{}/{}'.format(tempfile.mkdtemp(), '.authtoken')

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
        assert isinstance(client.experiment_group, ExperimentGroupApi)
        assert isinstance(client.experiment, ExperimentApi)
        assert isinstance(client.experiment_job, ExperimentJobApi)
        assert isinstance(client.job, JobApi)
        assert isinstance(client.build_job, BuildJobApi)
        assert isinstance(client.bookmark, BookmarkApi)
        assert isinstance(client.user, UserApi)

    def test_from_config(self):
        settings.SECRET_USER_TOKEN = 'token'  # noqa
        settings.API_HOST = 'localhost'
        client = PolyaxonClient(api_config=ApiConfig())
        assert client.is_managed is False
        assert client.host == 'localhost'
        assert client.http_port == 80
        assert client.ws_port == 80
        assert client.use_https is False
        assert client.token == 'token'
        assert client.api_config.http_host == 'http://localhost:80'
        assert client.api_config.ws_host == 'ws://localhost:80'

        settings.IS_MANAGED = True
        settings.API_HTTP_HOST = 'api_host'
        settings.API_WS_HOST = 'ws_host'
        settings.API_HOST = None
        client = PolyaxonClient(api_config=ApiConfig())
        assert client.is_managed is True
        assert client.host is None
        assert client.http_port == 80
        assert client.ws_port == 80
        assert client.use_https is False
        assert client.token == 'token'
        assert client.api_config.http_host == 'api_host'
        assert client.api_config.ws_host == 'ws_host'

    def test_from_env(self):
        settings.IS_MANAGED = False
        with self.assertRaises(PolyaxonClientException):
            PolyaxonClient()

        settings.SECRET_USER_TOKEN = 'token'  # noqa
        settings.API_HOST = 'localhost'
        client = PolyaxonClient()
        assert client.is_managed is False
        assert client.host == 'localhost'
        assert client.http_port == 80
        assert client.ws_port == 80
        assert client.use_https is False
        assert client.token == 'token'
        assert client.api_config.http_host == 'http://localhost:80'
        assert client.api_config.ws_host == 'ws://localhost:80'

        settings.IS_MANAGED = True
        settings.API_HTTP_HOST = 'api_host'
        settings.API_WS_HOST = 'ws_host'
        settings.API_HOST = None
        client = PolyaxonClient()
        assert client.is_managed is True
        assert client.host is None
        assert client.http_port == 80
        assert client.ws_port == 80
        assert client.use_https is False
        assert client.token == 'token'
        assert client.api_config.http_host == 'api_host'
        assert client.api_config.ws_host == 'ws_host'
