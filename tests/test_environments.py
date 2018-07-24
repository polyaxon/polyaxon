# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError
from tests.utils import assert_equal_dict

from polyaxon_schemas.environments import (
    EnvironmentConfig,
    GPUOptionsConfig,
    HorovodClusterConfig,
    HorovodConfig,
    K8SResourcesConfig,
    MXNetClusterConfig,
    MXNetConfig,
    PodResourcesConfig,
    PytorchClusterConfig,
    PytorchConfig,
    SessionConfig,
    TensorflowClusterConfig,
    TensorflowConfig,
    TFRunConfig
)
from polyaxon_schemas.utils import TaskType


class TestEnvironmentsConfigs(TestCase):
    def test_k8s_resources_config(self):
        config_dict = {
            'requests': 0.8,
            'limits': 1,
        }
        config = K8SResourcesConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

    def test_pod_resources_config(self):
        config_dict = {
            'cpu': {
                'requests': 0.8,
                'limits': 1
            },
            'gpu': {
                'requests': 2,
                'limits': 4
            },
            'memory': {
                'requests': 265,
                'limits': 512
            },
        }
        config = PodResourcesConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

    def test_pod_resources_add(self):
        config_dict1 = {
            'cpu': {
                'requests': 0.8,
            },
            'gpu': {
                'requests': 2,
            },
            'memory': {
                'requests': 200,
                'limits': 300
            },
        }

        config_dict2 = {
            'gpu': {
                'limits': 4
            },
            'memory': {
                'requests': 300,
                'limits': 200
            },
        }
        config1 = PodResourcesConfig.from_dict(config_dict1)
        config2 = PodResourcesConfig.from_dict(config_dict2)

        config = config1 + config2
        assert config.cpu.to_dict() == {'requests': 0.8, 'limits': None}
        assert config.memory.to_dict() == {'requests': 500, 'limits': 500}
        assert config.gpu.to_dict() == {'requests': 2, 'limits': 4}

    def test_gpu_options_config(self):
        config_dict = {
            'gpu_memory_fraction': 0.8,
            'allow_growth': False,
            'per_process_gpu_memory_fraction': 0.4,
        }
        config = GPUOptionsConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

    def test_session_config(self):
        config_dict = {
            'log_device_placement': False,
            'allow_soft_placement': False,
            'intra_op_parallelism_threads': 2,
            'inter_op_parallelism_threads': 3,
            'gpu_options': GPUOptionsConfig().to_dict(),
        }
        config = SessionConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_indexed_session(self):
        config_dict = {
            'index': 10,
            'log_device_placement': False,
            'allow_soft_placement': False,
            'intra_op_parallelism_threads': 2,
            'inter_op_parallelism_threads': 3,
            'gpu_options': GPUOptionsConfig().to_dict(),
        }
        config = SessionConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_tensorflow_cluster_config(self):
        config_dict = {
            "worker": [
                "worker0.example.com:2222",
                "worker1.example.com:2222",
                "worker2.example.com:2222"
            ],
            "ps": [
                "ps0.example.com:2222",
                "ps1.example.com:2222"
            ]
        }
        config = TensorflowClusterConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

    def test_horovod_cluster_config(self):
        config_dict = {
            "worker": [
                "worker0.example.com:2222",
                "worker1.example.com:2222",
                "worker2.example.com:2222"
            ]
        }
        config = HorovodClusterConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

    def test_pytorch_cluster_config(self):
        config_dict = {
            "worker": [
                "worker0.example.com:2222",
                "worker1.example.com:2222",
                "worker2.example.com:2222"
            ]
        }
        config = PytorchClusterConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

    def test_mxnet_cluster_config(self):
        config_dict = {
            "worker": [
                "worker0.example.com:2222",
                "worker1.example.com:2222",
                "worker2.example.com:2222"
            ],
            "server": [
                "server0.example.com:2222",
                "server1.example.com:2222"
            ]
        }
        config = MXNetClusterConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

    def test_run_config(self):
        config_dict = {
            'tf_random_seed': 100,
            'save_summary_steps': 100,
            'save_checkpoints_secs': 600,
            'save_checkpoints_steps': None,
            'keep_checkpoint_max': 5,
            'keep_checkpoint_every_n_hours': 10000,
        }
        config = TFRunConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add session config
        config_dict['session'] = SessionConfig().to_dict()
        config = TFRunConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add cluster config
        config_dict['cluster'] = TensorflowClusterConfig(
            worker=[TaskType.WORKER], ps=[TaskType.PS]
        ).to_dict()
        config = TFRunConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_tensorflow_config(self):
        config_dict = {
            'n_workers': 10,
            'n_ps': 5,
            'delay_workers_by_global_step': False
        }
        config = TensorflowConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add run config
        config_dict['run_config'] = TFRunConfig().to_dict()
        config = TensorflowConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add default worker session config
        config_dict['default_worker'] = {
            'config': SessionConfig(
                intra_op_parallelism_threads=1,
                inter_op_parallelism_threads=3).to_dict()
        }
        config = TensorflowConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add default worker resources
        config_dict['default_worker'] = {
            'resources': PodResourcesConfig(
                cpu=K8SResourcesConfig(0.5, 1),
                gpu=K8SResourcesConfig(2, 4)).to_dict()
        }
        config = TensorflowConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_light_dict())

        # Add default ps session config
        config_dict['default_ps'] = {
            'config': SessionConfig(
                intra_op_parallelism_threads=0,
                inter_op_parallelism_threads=2
            ).to_dict()
        }
        config = TensorflowConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_light_dict())

        # Add default ps resources
        config_dict['default_ps'] = {
            'resources': PodResourcesConfig(
                cpu=K8SResourcesConfig(0.5, 1),
                memory=K8SResourcesConfig(256, 400)).to_dict()
        }
        config = TensorflowConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_light_dict())

        # Adding custom config for worker 3
        config_dict['worker'] = [{
            'index': 3,
            'config': SessionConfig(
                gpu_options=GPUOptionsConfig(gpu_memory_fraction=0.4),
                intra_op_parallelism_threads=8,
                inter_op_parallelism_threads=8
            ).to_dict()
        }]
        config = TensorflowConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_light_dict())

        # Adding custom resources for worker 4
        config_dict['worker'] = [{
            'index': 4,
            'resources': PodResourcesConfig(
                cpu=K8SResourcesConfig(0.5, 1),
                memory=K8SResourcesConfig(256, 400),
            ).to_dict()
        }]
        config = TensorflowConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_light_dict())

        # Adding custom config for ps 2
        config_dict['ps'] = [{
            'index': 2,
            'config': SessionConfig(
                gpu_options=GPUOptionsConfig(allow_growth=False),
                intra_op_parallelism_threads=1,
                inter_op_parallelism_threads=1
            ).to_dict()
        }]
        config = TensorflowConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_light_dict())

        # Adding custom resources for ps 4
        config_dict['ps'] = [{
            'index': 4,
            'resources': PodResourcesConfig(
                cpu=K8SResourcesConfig(0.5, 1),
                memory=K8SResourcesConfig(256, 400)).to_dict()
        }]
        config = TensorflowConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_light_dict())

    def test_horovod_config(self):
        config_dict = {
            'n_workers': 10,
        }
        config = HorovodConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_light_dict())

        # Add default worker resources
        config_dict['default_worker'] = {
            'resources': PodResourcesConfig(
                cpu=K8SResourcesConfig(0.5, 1),
                gpu=K8SResourcesConfig(2, 4)).to_dict()
        }
        config = HorovodConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Adding custom resources for worker 4
        config_dict['worker'] = [{
            'index': 4,
            'resources': PodResourcesConfig(
                cpu=K8SResourcesConfig(0.5, 1),
                memory=K8SResourcesConfig(256, 400)).to_dict()
        }]
        config = HorovodConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_light_dict())

    def test_pytorch_config(self):
        config_dict = {
            'n_workers': 10,
        }
        config = PytorchConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add default worker resources
        config_dict['default_worker'] = {
            'resources': PodResourcesConfig(
                cpu=K8SResourcesConfig(0.5, 1),
                gpu=K8SResourcesConfig(2, 4)).to_dict()
        }
        config = PytorchConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Adding custom resources for worker 4
        config_dict['worker'] = [{
            'index': 4,
            'resources': PodResourcesConfig(cpu=K8SResourcesConfig(0.5, 1),
                                            memory=K8SResourcesConfig(256, 400)).to_dict()
        }]
        config = PytorchConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

    def test_mxnet_config(self):
        config_dict = {
            'n_workers': 10,
            'n_ps': 5,
        }
        config = MXNetConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add default worker resources
        config_dict['default_worker'] = {
            'resources': PodResourcesConfig(
                cpu=K8SResourcesConfig(0.5, 1),
                gpu=K8SResourcesConfig(2, 4)).to_dict()
        }
        config = MXNetConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add default ps resources
        config_dict['default_ps'] = {
            'resources': PodResourcesConfig(
                cpu=K8SResourcesConfig(0.5, 1),
                memory=K8SResourcesConfig(256, 400)).to_dict()
        }
        config = MXNetConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Adding custom resources for worker 4
        config_dict['worker'] = [{
            'index': 4,
            'resources': PodResourcesConfig(
                cpu=K8SResourcesConfig(0.5, 1),
                memory=K8SResourcesConfig(256, 400)).to_dict()
        }]
        config = MXNetConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Adding custom resources for ps 4
        config_dict['ps'] = [{
            'index': 4,
            'resources': PodResourcesConfig(
                cpu=K8SResourcesConfig(0.5, 1),
                memory=K8SResourcesConfig(256, 400)).to_dict()
        }]
        config = MXNetConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

    def test_environment_config(self):
        config_dict = {
            'resources': PodResourcesConfig(cpu=K8SResourcesConfig(0.5, 1)).to_dict()
        }
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add node selectors
        config_dict['node_selector'] = {
            'polyaxon.com': 'master',
        }

        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add persistence
        config_dict['persistence'] = {
            'data': ['data1', 'data2'],
            'outputs': 'outputs1',
        }
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add outputs
        config_dict['outputs'] = {
            'jobs': ['data1.dfs', 34, 'data2'],
            'experiments': [1, 'outputs1', 2, 3],
        }
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add tensorflow
        config_dict['tensorflow'] = {
            'n_workers': 10,
            'n_ps': 5,
        }

        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add mxnet should raise
        config_dict['mxnet'] = {
            'n_workers': 10,
            'n_ps': 5,
        }

        with self.assertRaises(ValidationError):
            EnvironmentConfig.from_dict(config_dict)

        # Removing tensorflow should pass for mxnet
        del config_dict['tensorflow']
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Adding horovod should raise
        config_dict['horovod'] = {
            'n_workers': 5
        }

        with self.assertRaises(ValidationError):
            EnvironmentConfig.from_dict(config_dict)

        # Removing mxnet should pass for horovod
        del config_dict['mxnet']
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Adding pytorch should raise
        config_dict['pytorch'] = {
            'n_workers': 5
        }

        with self.assertRaises(ValidationError):
            EnvironmentConfig.from_dict(config_dict)

        # Removing horovod should pass for pytorch
        del config_dict['horovod']
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())
