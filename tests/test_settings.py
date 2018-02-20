# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.logging import LoggingConfig
from polyaxon_schemas.settings import (
    GPUOptionsConfig,
    RunConfig,
    SessionConfig,
    ClusterConfig,
    EnvironmentConfig,
    SettingsConfig,
    K8SResourcesConfig,
    PodResourcesConfig,
    EarlyStoppingMetricConfig,
)
from polyaxon_schemas.utils import TaskType, SEARCH_METHODS

from tests.utils import assert_equal_dict


class TestSettingConfigs(TestCase):
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

    def test_cluster_config(self):
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
        config = ClusterConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_run_config(self):
        config_dict = {
            'tf_random_seed': 100,
            'save_summary_steps': 100,
            'save_checkpoints_secs': 600,
            'save_checkpoints_steps': None,
            'keep_checkpoint_max': 5,
            'keep_checkpoint_every_n_hours': 10000,
        }
        config = RunConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add session config
        config_dict['session'] = SessionConfig().to_dict()
        config = RunConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add cluster config
        config_dict['cluster'] = ClusterConfig(
            worker=[TaskType.WORKER], ps=[TaskType.PS]
        ).to_dict()
        config = RunConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_environment_config(self):
        config_dict = {
            'n_workers': 10,
            'n_ps': 5,
            'delay_workers_by_global_step': False
        }
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add run config
        config_dict['run_config'] = RunConfig().to_dict()
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add run resources
        config_dict['resources'] = PodResourcesConfig(
            cpu=K8SResourcesConfig(0.5, 1)).to_dict()
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add default worker session config
        config_dict['default_worker_config'] = SessionConfig(
            intra_op_parallelism_threads=1,
            inter_op_parallelism_threads=3
        ).to_dict()
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add default worker resources
        config_dict['default_worker_resources'] = PodResourcesConfig(
            cpu=K8SResourcesConfig(0.5, 1), gpu=K8SResourcesConfig(2, 4)).to_dict()
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add default ps session config
        config_dict['default_wps_config'] = SessionConfig(
            intra_op_parallelism_threads=0,
            inter_op_parallelism_threads=2
        ).to_dict()
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add default ps resources
        config_dict['default_ps_resources'] = PodResourcesConfig(
            cpu=K8SResourcesConfig(0.5, 1), memory=K8SResourcesConfig(256, 400)).to_dict()
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Adding custom config for worker 3
        config_dict['worker_configs'] = [SessionConfig(
            index=3,
            gpu_options=GPUOptionsConfig(gpu_memory_fraction=0.4),
            intra_op_parallelism_threads=8,
            inter_op_parallelism_threads=8
        ).to_dict()]
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Adding custom resources for worker 4
        config_dict['worker_resources'] = [PodResourcesConfig(
            index=4, cpu=K8SResourcesConfig(0.5, 1), memory=K8SResourcesConfig(256, 400)).to_dict()]
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Adding custom config for ps 2
        config_dict['ps_configs'] = [SessionConfig(
            index=2,
            gpu_options=GPUOptionsConfig(allow_growth=False),
            intra_op_parallelism_threads=1,
            inter_op_parallelism_threads=1
        ).to_dict()]
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Adding custom resources for ps 4
        config_dict['ps_resources'] = [PodResourcesConfig(
            index=4, cpu=K8SResourcesConfig(0.5, 1), memory=K8SResourcesConfig(256, 400)).to_dict()]
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_early_stopping(self):
        config_dict = {
            'metric': 'loss',
            'value': 0.1,
            'higher': False
        }
        config = EarlyStoppingMetricConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_settings_config(self):
        config_dict = {
            'logging': LoggingConfig().to_dict(),
            'export_strategies': None,
            'run_type': 'local',
            'concurrent_experiments': 2,
            'search_method': SEARCH_METHODS.RANDOM
        }
        config = SettingsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add n_experiments
        config_dict['n_experiments'] = 10
        config = SettingsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Add early stopping
        config_dict['early_stopping'] = [
            {
                'metric': 'loss',
                'value': 0.1,
                'higher': False
            },
            {
                'metric': 'accuracy',
                'value': 0.9,
                'higher': True
            }
        ]
        config = SettingsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
