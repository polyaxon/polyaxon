# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_client.auth import AuthClient
from polyaxon_client.bookmark import BookmarkClient
from polyaxon_client.build_job import BuildJobClient
from polyaxon_client.clients import PolyaxonClients
from polyaxon_client.cluster import ClusterClient
from polyaxon_client.experiment import ExperimentClient
from polyaxon_client.experiment_group import ExperimentGroupClient
from polyaxon_client.experiment_job import ExperimentJobClient
from polyaxon_client.job import JobClient
from polyaxon_client.project import ProjectClient
from polyaxon_client.user import UserClient
from polyaxon_client.version import VersionClient


class TestPolyaxonClients(TestCase):
    def test_clients(self):
        clients = PolyaxonClients(host=None, token=None)
        assert clients.host is None
        assert clients.http_port == 80
        assert clients.ws_port == 80
        assert clients.use_https is False
        assert clients.token is None

        assert isinstance(clients.auth, AuthClient)
        assert isinstance(clients.cluster, ClusterClient)
        assert isinstance(clients.version, VersionClient)
        assert isinstance(clients.project, ProjectClient)
        assert isinstance(clients.experiment_group, ExperimentGroupClient)
        assert isinstance(clients.experiment, ExperimentClient)
        assert isinstance(clients.experiment_job, ExperimentJobClient)
        assert isinstance(clients.job, JobClient)
        assert isinstance(clients.build_job, BuildJobClient)
        assert isinstance(clients.bookmark, BookmarkClient)
        assert isinstance(clients.user, UserClient)
