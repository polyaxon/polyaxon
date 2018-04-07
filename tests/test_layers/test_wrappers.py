# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_layers

from polyaxon_schemas.layers.embeddings import EmbeddingConfig
from polyaxon_schemas.layers.wrappers import (
    BidirectionalConfig,
    TimeDistributedConfig,
    WrapperConfig
)


class TestWrapperConfigs(TestCase):
    @staticmethod
    def assert_wrapper_config(wrapper_class):
        config_dict = {
            'layer': EmbeddingConfig(input_dim=30, output_dim=30).to_schema(),
        }
        config = wrapper_class.from_dict(config_dict)
        assert_equal_layers(config, config_dict)

    def test_wrapper_config(self):
        self.assert_wrapper_config(WrapperConfig)
        self.assert_wrapper_config(TimeDistributedConfig)
        self.assert_wrapper_config(BidirectionalConfig)
