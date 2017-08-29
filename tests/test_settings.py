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
    SettingsConfig
)
from tests.utils import assert_equal_dict


class TestSettingConfigs(TestCase):
    def test_gpu_options_config(self):
        config_dict = {
            'gpu_memory_fraction': False
        }
        config = GPUOptionsConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert_equal_dict(config_to_dict, config_dict)

    def test_session_config(self):
        config_dict = {
            'log_device_placement': False,
            'allow_soft_placement': False,
            'allow_growth': False,
            'gpu_options': GPUOptionsConfig().to_dict(),
        }
        config = SessionConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert_equal_dict(config_to_dict, config_dict)

    def test_run_config(self):
        config_dict = {
            'num_cores': 0,
            'tf_random_seed': None,
            'save_summary_steps': 100,
            'save_checkpoints_secs': 600,
            'save_checkpoints_steps': None,
            'keep_checkpoint_max': 5,
            'keep_checkpoint_every_n_hours': 10000,
            'model_dir': 'some_path'
        }
        config = RunConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()

        assert_equal_dict(config_to_dict, config_dict)

        config_dict['session_config'] = SessionConfig().to_dict()
        config = RunConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()

        assert_equal_dict(config_to_dict, config_dict)

        config_dict['cluster_config'] = ClusterConfig().to_dict()
        config = RunConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert_equal_dict(config_to_dict, config_dict)

    def test_environment_config(self):
        config_dict = {
            'type': 'local',
            'distributed': True,
            'n_workers': 10,
            'n_ps': 5,
            'delay_workers_by_global_step': False
        }
        config = EnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_settings_config(self):
        config_dict = {
            'logging': LoggingConfig().to_dict(),
            'train_strategy': None,
            'export_strategies': None,
            'environment': EnvironmentConfig().to_dict()
        }
        config = SettingsConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
