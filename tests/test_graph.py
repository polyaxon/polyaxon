# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from tests.utils import assert_equal_graphs

from polyaxon_schemas.graph import GraphConfig


class TestGraphConfigs(TestCase):
    def test_graph_config(self):
        config_dict = {
            'input_layers': ['image'],
            'output_layers': [['dense_0', 0, 0]],
            'layers': [
                {
                    'Conv2D': {
                        'filters': 64,
                        'strides': [1, 1],
                        'kernel_size': [2, 2],
                        'activation': 'relu',
                        'name': 'convolution_1',
                    }
                },
                {'Dense': {'units': 17, 'name': 'dense_0'}}
            ]
        }
        config = GraphConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert_equal_graphs(config_dict, config_to_dict)
