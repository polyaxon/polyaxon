# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_client.auth import AuthClient
from polyaxon_client.bookmark import BookmarkClient
from polyaxon_client.build_job import BuildJobClient
from polyaxon_client.client import PolyaxonClient
from polyaxon_client.cluster import ClusterClient
from polyaxon_client.experiment import ExperimentClient
from polyaxon_client.experiment_group import ExperimentGroupClient
from polyaxon_client.experiment_job import ExperimentJobClient
from polyaxon_client.job import JobClient
from polyaxon_client.project import ProjectClient
from polyaxon_client.user import UserClient
from polyaxon_client.version import VersionClient


class TestPolyaxonClient(TestCase):
    def test_client(self):
        client = PolyaxonClient(host=None, token=None)
        assert client.host is None
        assert client.http_port == 80
        assert client.ws_port == 80
        assert client.use_https is False
        assert client.token is None

        assert isinstance(client.auth, AuthClient)
        assert isinstance(client.cluster, ClusterClient)
        assert isinstance(client.version, VersionClient)
        assert isinstance(client.project, ProjectClient)
        assert isinstance(client.experiment_group, ExperimentGroupClient)
        assert isinstance(client.experiment, ExperimentClient)
        assert isinstance(client.experiment_job, ExperimentJobClient)
        assert isinstance(client.job, JobClient)
        assert isinstance(client.build_job, BuildJobClient)
        assert isinstance(client.bookmark, BookmarkClient)
        assert isinstance(client.user, UserClient)
