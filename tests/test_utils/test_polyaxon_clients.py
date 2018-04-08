# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch
from unittest import TestCase

from polyaxon_cli.utils.clients import PolyaxonClients
from polyaxon_client.auth import AuthClient
from polyaxon_client.cluster import ClusterClient
from polyaxon_client.experiment import ExperimentClient
from polyaxon_client.experiment_group import ExperimentGroupClient
from polyaxon_client.jobs import JobClient
from polyaxon_client.project import ProjectClient
from polyaxon_client.user import UserClient
from polyaxon_client.version import VersionClient


class TestPolyaxonClients(TestCase):
    @patch('polyaxon_cli.utils.clients.GlobalConfigManager.get_value')
    @patch('polyaxon_cli.utils.clients.AuthConfigManager.get_value')
    def test_clients(self, get_value_mock1, get_value_mock2):
        get_value_mock1.return_value = None
        get_value_mock2.return_value = None

        clients = PolyaxonClients()
        assert clients.host is None
        assert clients.http_port is None
        assert clients.ws_port is None
        assert clients.use_https is None
        assert clients.token is None

        assert isinstance(clients.auth, AuthClient)
        assert isinstance(clients.cluster, ClusterClient)
        assert isinstance(clients.version, VersionClient)
        assert isinstance(clients.project, ProjectClient)
        assert isinstance(clients.experiment_group, ExperimentGroupClient)
        assert isinstance(clients.experiment, ExperimentClient)
        assert isinstance(clients.job, JobClient)
        assert isinstance(clients.user, UserClient)
