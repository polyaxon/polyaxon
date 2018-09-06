# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import httpretty
import json
import uuid

from tests.test_api.utils import TestBaseApi

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.api.cluster import ClusterApi
from polyaxon_client.schemas import ClusterNodeConfig, PolyaxonClusterConfig


class TestClusterApi(TestBaseApi):

    def setUp(self):
        super(TestClusterApi, self).setUp()
        self.api_handler = ClusterApi(transport=self.transport, config=self.api_config)

    @httpretty.activate
    def test_get_cluster(self):
        obj = PolyaxonClusterConfig(version_api={}).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/cluster'),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.get_cluster()
        assert result.to_dict() == obj

        # Raw response
        self.set_raw_response()
        result = self.api_handler.get_cluster()
        assert result == obj

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
                                status=1).to_dict()

        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/nodes',
                1),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.get_node(1)
        assert result.to_dict() == obj

        # Raw response
        self.set_raw_response()
        result = self.api_handler.get_node(1)
        assert result == obj
