# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import random
import uuid

from unittest import TestCase

from polyaxon_schemas.clusters import ClusterNodeConfig, NodeGPUConfig, PolyaxonClusterConfig


class TestClusterConfigs(TestCase):

    @staticmethod
    def create_gpu():
        return {
            'uuid': uuid.uuid4().hex,
            'serial': 'serial',
            'name': 'gamma',
            'index': random.randint(1, 100),
            'memory': 10,
            'cluster_node': uuid.uuid4().hex
        }

    @classmethod
    def create_cluster_node(cls):
        return {
            'uuid': uuid.uuid4().hex,
            'sequence': 1,
            'name': 'node',
            'hostname': 'hostname',
            'role': 'master',
            'docker_version': 'v1',
            'kubelet_version': 'v1',
            'os_image': 'some image',
            'kernel_version': 'v1',
            'schedulable_taints': True,
            'schedulable_state': True,
            'memory': 10,
            'cpu': 2,
            'n_gpus': 3,
            'status': 'Running',
            'gpus': [cls.create_gpu()]
        }

    def test_node_gpu_config(self):
        config_dict = self.create_gpu()
        config = NodeGPUConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_cluster_node_config(self):
        config_dict = self.create_cluster_node()
        config = ClusterNodeConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_plx_cluster_config(self):
        config_dict = {
            'version_api': {},
            'nodes': [self.create_cluster_node(), self.create_cluster_node()]
        }
        config = PolyaxonClusterConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
