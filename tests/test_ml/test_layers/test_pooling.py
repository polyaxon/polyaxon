# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_layers

from polyaxon_schemas.ml.layers.pooling import (
    AveragePooling1DConfig,
    AveragePooling2DConfig,
    AveragePooling3DConfig,
    GlobalAveragePooling1DConfig,
    GlobalAveragePooling2DConfig,
    GlobalAveragePooling3DConfig,
    GlobalMaxPooling1DConfig,
    GlobalMaxPooling2DConfig,
    GlobalMaxPooling3DConfig,
    MaxPooling1DConfig,
    MaxPooling2DConfig,
    MaxPooling3DConfig
)


class TestPoolingConfigs(TestCase):
    @staticmethod
    def assert_pooling_config(pooling_class, dim):
        config_dict = {
            'pool_size': 1 if dim == 1 else [1, 1] if dim == 2 else [1, 1, 1],
            'strides': 1 if dim == 1 else [1, 1] if dim == 2 else [1, 1, 1],
            'padding': 'valid',
        }
        if dim > 1:
            config_dict['data_format'] = None
        config = pooling_class.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    @staticmethod
    def assert_global_pooling_config(pooling_class, dim):
        config_dict = {}
        if dim > 1:
            config_dict['data_format'] = None
        config = pooling_class.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_pooling_config(self):
        self.assert_pooling_config(MaxPooling1DConfig, 1)
        self.assert_pooling_config(AveragePooling1DConfig, 1)
        self.assert_pooling_config(MaxPooling2DConfig, 2)
        self.assert_pooling_config(AveragePooling2DConfig, 2)
        self.assert_pooling_config(MaxPooling3DConfig, 3)
        self.assert_pooling_config(AveragePooling3DConfig, 3)

    def test_global_pooling_config(self):
        self.assert_global_pooling_config(GlobalAveragePooling1DConfig, 1)
        self.assert_global_pooling_config(GlobalMaxPooling1DConfig, 1)
        self.assert_global_pooling_config(GlobalAveragePooling2DConfig, 2)
        self.assert_global_pooling_config(GlobalMaxPooling2DConfig, 2)
        self.assert_global_pooling_config(GlobalAveragePooling3DConfig, 3)
        self.assert_global_pooling_config(GlobalMaxPooling3DConfig, 3)
