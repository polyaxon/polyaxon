# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_dict, assert_tensors

from polyaxon_schemas.losses import (
    AbsoluteDifferenceConfig,
    ClippedDeltaLossConfig,
    CosineDistanceConfig,
    HingeLossConfig,
    HuberLossConfig,
    KullbackLeiberDivergenceConfig,
    LogLossConfig,
    MeanSquaredErrorConfig,
    PoissonLossConfig,
    SigmoidCrossEntropyConfig,
    SoftmaxCrossEntropyConfig
)


class TestLossConfigs(TestCase):
    @staticmethod
    def assert_equal_losses(l1, l2):
        assert_tensors(l1.pop('input_layer', None), l2.pop('input_layer', None))
        assert_tensors(l1.pop('output_layer', None), l2.pop('output_layer', None))

        assert_equal_dict(l1, l2)
    
    def test_base_losses_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'weights': 1.0,
            'name': 'l',
            'collect': False
        }

        config_classes = [
            AbsoluteDifferenceConfig,
            MeanSquaredErrorConfig,
            HingeLossConfig
        ]

        for config_class in config_classes:
            config = config_class.from_dict(config_dict)
            self.assert_equal_losses(config.to_dict(), config_dict)

    def test_log_loss_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'epsilon': 0.0001,
            'weights': 1.0,
            'name': 'l',
            'collect': False
        }
        config = LogLossConfig.from_dict(config_dict)
        self.assert_equal_losses(config.to_dict(), config_dict)

    def test_clipped_loss_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'clip_value_min': -0.1,
            'clip_value_max': -0.1,
            'weights': 1.0,
            'name': 'l',
            'collect': False
        }
        config = ClippedDeltaLossConfig.from_dict(config_dict)
        self.assert_equal_losses(config.to_dict(), config_dict)

    def test_huber_loss_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'clip': 0.1,
            'weights': 1.0,
            'name': 'l',
            'collect': False
        }
        config = HuberLossConfig.from_dict(config_dict)
        self.assert_equal_losses(config.to_dict(), config_dict)

    def test_softmax_crossentropy_loss_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'label_smoothing': 0.,
            'weights': 1.0,
            'name': 'l',
            'collect': False
        }
        config = SoftmaxCrossEntropyConfig.from_dict(config_dict)
        self.assert_equal_losses(config.to_dict(), config_dict)

    def test_sigmoid_crossentropy_loss_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'label_smoothing': 0.,
            'weights': 1.0,
            'name': 'l',
            'collect': False
        }
        config = SigmoidCrossEntropyConfig.from_dict(config_dict)
        self.assert_equal_losses(config.to_dict(), config_dict)

    def test_cosine_distance_loss_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'dim': 0,
            'weights': 1.0,
            'name': 'l',
            'collect': False
        }
        config = CosineDistanceConfig.from_dict(config_dict)
        self.assert_equal_losses(config.to_dict(), config_dict)

    def test_poisson_loss_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'weights': 1.0,
            'name': 'l',
            'collect': False
        }
        config = PoissonLossConfig.from_dict(config_dict)
        self.assert_equal_losses(config.to_dict(), config_dict)

    def test_kullbackleiber_div_loss_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'dim': 0,
            'weights': 1.0,
            'name': 'l',
            'collect': False
        }
        config = KullbackLeiberDivergenceConfig.from_dict(config_dict)
        self.assert_equal_losses(config.to_dict(), config_dict)
