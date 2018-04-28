# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import httpretty
import json
import uuid

from faker import Faker
from unittest import TestCase

from polyaxon_client.cluster import ClusterClient
from polyaxon_schemas.clusters import ClusterNodeConfig, PolyaxonClusterConfig

faker = Faker()


class TestClusterClient(TestCase):
    def setUp(self):
        self.client = ClusterClient(host='localhost',
                                    http_port=8000,
                                    ws_port=1337,
                                    version='v1',
                                    token=faker.uuid4(),
                                    reraise=True)

    @httpretty.activate
    def test_get_cluster(self):
        obj = PolyaxonClusterConfig(version_api={})
        httpretty.register_uri(
            httpretty.GET,
            ClusterClient._build_url(
                self.client.base_url,
                ClusterClient.ENDPOINT),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.get_cluster()
        assert result.to_dict() == obj.to_dict()

    @httpretty.activate
    def test_get_node(self):
        obj = ClusterNodeConfig(uuid=uuid.uuid4().hex,
                                name='name',
                                hostname='hostname',
                                role='Master',
                                docker_version='v1',
                                kubelet_version='v1',
                                os_image='image',
                                kernel_version='v1',
                                schedulable_taints=True,
                                schedulable_state=True,
                                memory=10,
                                cpu=2,
                                n_gpus=1,
                                status=1)

        httpretty.register_uri(
            httpretty.GET,
            ClusterClient._build_url(
                self.client.base_url,
                ClusterClient.ENDPOINT_NODES,
                1),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.get_node(1)
        assert result.to_dict() == obj.to_dict()
