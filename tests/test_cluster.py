# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import uuid
from unittest import TestCase
import httpretty
from faker import Faker

from polyaxon_schemas.clusters import PolyaxonClusterConfig, ClusterNodeConfig

from polyaxon_client.cluster import ClusterClient

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
    def test_list_clusters(self):
        cluster_uuid = uuid.uuid4().hex
        user_uuid = uuid.uuid4().hex
        xps = [PolyaxonClusterConfig(uuid=cluster_uuid,
                                     user=user_uuid,
                                     version_api={}).to_dict()
               for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ClusterClient._build_url(
                self.client.base_url,
                ClusterClient.ENDPOINT),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        xps_results = self.client.list_clusters()
        assert len(xps_results) == 10

        # pagination
        httpretty.register_uri(
            httpretty.GET,
            ClusterClient._build_url(
                self.client.base_url,
                ClusterClient.ENDPOINT) + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        xps_results = self.client.list_clusters(page=2)
        assert len(xps_results) == 10

    @httpretty.activate
    def test_get_cluster(self):
        cluster_uuid = uuid.uuid4().hex
        user_uuid = uuid.uuid4().hex
        object = PolyaxonClusterConfig(uuid=cluster_uuid,
                                       user=user_uuid,
                                       version_api={})
        httpretty.register_uri(
            httpretty.GET,
            ClusterClient._build_url(
                self.client.base_url,
                ClusterClient.ENDPOINT,
                cluster_uuid),
            body=json.dumps(object.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.get_cluster(cluster_uuid)
        assert result.to_dict() == object.to_dict()

    @httpretty.activate
    def test_get_node(self):
        node_uuid = uuid.uuid4().hex
        object = ClusterNodeConfig(uuid=node_uuid,
                                   name='name',
                                   cluster=uuid.uuid4().hex,
                                   hostname='hostname',
                                   role='Master',
                                   docker_version='v1',
                                   kubelet_version='v1',
                                   os_image='image',
                                   kernel_version='v1',
                                   schedulable_taints=True,
                                   schedulable_state=True,
                                   memory=10,
                                   n_cpus=2,
                                   n_gpus=1,
                                   status=1)

        httpretty.register_uri(
            httpretty.GET,
            ClusterClient._build_url(
                self.client.base_url,
                ClusterClient.ENDPOINT_NODES,
                node_uuid),
            body=json.dumps(object.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.get_node(node_uuid)
        assert result.to_dict() == object.to_dict()
