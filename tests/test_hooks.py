# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_dict

from polyaxon_schemas.hooks import (
    EpisodeLoggingTensorHookConfig,
    FinalOpsHookConfig,
    GlobalStepWaiterHookConfig,
    StepLoggingTensorHookConfig
)


class TestHookConfigs(TestCase):
    def test_global_step_wait_hook_config(self):
        config_dict = {
            'wait_until_step': 10
        }
        config = GlobalStepWaiterHookConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert_equal_dict(config_to_dict, config_dict)

    def test_final_ops_hook_config(self):
        config_dict = {
            'final_ops': ['loss', 'precision']
        }
        config = FinalOpsHookConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert_equal_dict(config_to_dict, config_dict)

    def test_step_logging_tensor_hook(self):
        config_dict = {
            'tensors': ['conv2d_1', 'relu_1'],
            'every_n_iter': 10,
            'every_n_secs': None
        }
        config = StepLoggingTensorHookConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert_equal_dict(config_to_dict, config_dict)

    def test_episode_logging_tensor_hook(self):
        config_dict = {
            'tensors': ['conv2d_1', 'relu_1'],
            'every_n_episodes': 2,
        }
        config = EpisodeLoggingTensorHookConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert_equal_dict(config_to_dict, config_dict)
