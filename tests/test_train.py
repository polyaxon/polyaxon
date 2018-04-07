# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_dict

from polyaxon_schemas.hooks import StepLoggingTensorHookConfig
from polyaxon_schemas.processing.pipelines import TFRecordSequencePipelineConfig
from polyaxon_schemas.train import TrainConfig


class TestTrainConfigs(TestCase):
    def test_train_config(self):
        config_dict = {
            'data_pipeline': TFRecordSequencePipelineConfig(
                data_files=['~/data_file'],
                meta_data_file='~/meta_data_file',
                shuffle=True,
                num_epochs=10,
                batch_size=64).to_schema(),
            'steps': 300,
            'hooks': [
                StepLoggingTensorHookConfig(['Dense_1', 'Conv2D_4'], every_n_iter=100).to_schema()
            ]
        }
        config = TrainConfig.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)
