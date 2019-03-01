# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_dict, assert_tensors

from polyaxon_schemas.ml.metrics import (
    AccuracyConfig,
    AUCConfig,
    CovarianceConfig,
    FalseNegativesConfig,
    FalsePositivesConfig,
    MeanAbsoluteErrorConfig,
    MeanConfig,
    MeanCosineDistanceConfig,
    MeanIOUConfig,
    MeanRelativeErrorConfig,
    MeanSquaredErrorConfig,
    MeanTensorConfig,
    PearsonCorrelationConfig,
    PercentageLessConfig,
    PrecisionAtThresholdsConfig,
    PrecisionConfig,
    RecallAtThresholdsConfig,
    RecallConfig,
    RootMeanSquaredErrorConfig,
    SensitivityAtSpecificityConfig,
    SparsePrecisionAtKConfig,
    SpecificityAtSensitivityConfig,
    TrueNegativesConfig,
    TruePositivesConfig
)


class TestMetricConfigs(TestCase):
    @staticmethod
    def assert_equal_metrics(m1, m2):
        assert_tensors(m1.pop('input_layer', None), m2.pop('input_layer', None))
        assert_tensors(m1.pop('output_layer', None), m2.pop('output_layer', None))

        assert_equal_dict(m1, m2)

    def test_base_metrics_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'weights': None,
            'name': 'm'
        }

        config_classes = [
            TruePositivesConfig,
            TrueNegativesConfig,
            FalsePositivesConfig,
            FalseNegativesConfig,
            AccuracyConfig,
            PrecisionConfig,
            RecallConfig,
            MeanAbsoluteErrorConfig,
            MeanSquaredErrorConfig,
            RootMeanSquaredErrorConfig,
            CovarianceConfig,
            PearsonCorrelationConfig,
        ]

        for config_class in config_classes:
            config = config_class.from_dict(config_dict)
            self.assert_equal_metrics(config.to_dict(), config_dict)

    def test_auc_metric_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'num_thresholds': 300,
            'weights': None,
            'curve': 'ROC',
            'name': 'm',
        }
        config = AUCConfig.from_dict(config_dict)
        self.assert_equal_metrics(config.to_dict(), config_dict)

    def test_mean_metric_config(self):
        config_dicts = [
            {
                'values': ['images', 0, 0],
                'weights': None,
                'name': 'm'
            },
            {
                'values': ['images', 0, 0],
                'weights': None,
                'name': 'm'
            }
        ]

        for config_dict in config_dicts:
            config = MeanConfig.from_dict(config_dict)
            self.assert_equal_metrics(config.to_dict(), config_dict)

    def test_mean_tensor_metric_config(self):
        config_dicts = [
            {
                'values': ['images', 0, 0],
                'weights': None,
                'name': 'm'
            },
            {
                'values': ['images', 0, 0],
                'weights': None,
                'name': 'm'
            }
        ]

        for config_dict in config_dicts:
            config = MeanTensorConfig.from_dict(config_dict)
            self.assert_equal_metrics(config.to_dict(), config_dict)

    def test_specificity_at_sensitivity_metric_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'sensitivity': 0.1,
            'num_thresholds': 300,
            'weights': None,
            'name': 'm'
        }
        config = SpecificityAtSensitivityConfig.from_dict(config_dict)
        self.assert_equal_metrics(config.to_dict(), config_dict)

    def test_sensitivity_at_specificity_metric_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'specificity': 0.1,
            'num_thresholds': 300,
            'weights': None,
            'name': 'm'
        }
        config = SensitivityAtSpecificityConfig.from_dict(config_dict)
        self.assert_equal_metrics(config.to_dict(), config_dict)

    def test_metric_at_thresholds_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'thresholds': [0.1, 0.1, 0.1],
            'weights': None,
            'name': 'm'
        }
        config_classes = [PrecisionAtThresholdsConfig, RecallAtThresholdsConfig]
        for config_class in config_classes:
            config = config_class.from_dict(config_dict)
            self.assert_equal_metrics(config.to_dict(), config_dict)

    def test_sparse_precistion_at_k_metric_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'k': 1,
            'class_id': None,
            'weights': None,
            'name': 'm'
        }
        config = SparsePrecisionAtKConfig.from_dict(config_dict)
        self.assert_equal_metrics(config.to_dict(), config_dict)

    def test_mean_relative_error_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'normalizer': 'tensor_normalizer',
            'weights': None,
            'name': 'm'
        }
        config = MeanRelativeErrorConfig.from_dict(config_dict)
        self.assert_equal_metrics(config.to_dict(), config_dict)

    def test_mean_consine_distance_metric_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'dim': 1,
            'weights': None,
            'name': 'm'
        }
        config = MeanCosineDistanceConfig.from_dict(config_dict)
        self.assert_equal_metrics(config.to_dict(), config_dict)

    def test_percentage_less_metric_config(self):
        config_dict = {
            'values': ['images', 0, 0],
            'threshold': 0.4,
            'weights': None,
            'name': 'm'
        }
        config = PercentageLessConfig.from_dict(config_dict)
        self.assert_equal_metrics(config.to_dict(), config_dict)

    def test_mean_iou_config(self):
        config_dict = {
            'input_layer': 'images',
            'output_layer': 'relu_1',
            'num_classes': 4,
            'weights': None,
            'name': 'm'
        }
        config = MeanIOUConfig.from_dict(config_dict)
        self.assert_equal_metrics(config.to_dict(), config_dict)
