# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_dict

from polyaxon_schemas.ops.environments.legacy import GPUOptionsConfig, SessionConfig, TFRunConfig
from polyaxon_schemas.ops.experiment.environment import TensorflowClusterConfig
from polyaxon_schemas.utils import TaskType


class TestLegacyConfigs(TestCase):

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
            'log_device_placement': False,
            'allow_soft_placement': False,
            'intra_op_parallelism_threads': 2,
            'inter_op_parallelism_threads': 3,
            'gpu_options': GPUOptionsConfig().to_dict(),
        }
        config = SessionConfig.from_dict(config_dict)
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
