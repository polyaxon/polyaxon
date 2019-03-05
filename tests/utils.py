# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from collections import Mapping


def assert_equal_dict(dict1, dict2):
    for k, v in six.iteritems(dict1):
        if v is None:
            continue
        if isinstance(v, Mapping):
            assert_equal_dict(v, dict2[k])
        else:
            assert v == dict2[k]


def assert_equal_feature_processors(fp1, fp2):
    # Check that they have same features
    assert list(six.iterkeys(fp1)) == list(six.iterkeys(fp2))

    # Check that all features have the same graph
    for feature in fp1:
        assert_equal_graphs(fp2[feature], fp1[feature])


def assert_tensors(tensor1, tensor2):
    if isinstance(tensor1, six.string_types):
        tensor1 = [tensor1, 0, 0]

    if isinstance(tensor2, six.string_types):
        tensor2 = [tensor2, 0, 0]

    assert tensor1 == tensor2


def assert_equal_graphs(result_graph, expected_graph):
    for i, input_layer in enumerate(expected_graph['input_layers']):
        assert_tensors(input_layer, result_graph['input_layers'][i])

    for i, output_layer in enumerate(expected_graph['output_layers']):
        assert_tensors(output_layer, result_graph['output_layers'][i])

    for layer_i, layer in enumerate(result_graph['layers']):
        layer_name, layer_data = list(six.iteritems(layer))[0]
        assert layer_name in expected_graph['layers'][layer_i]
        for k, v in six.iteritems(layer_data):
            assert v == expected_graph['layers'][layer_i][layer_name][k]


def assert_equal_layers(config, expected_layer):
    result_layer = config.to_dict()
    for k, v in six.iteritems(expected_layer):
        if v is not None or k not in config.REDUCED_ATTRIBUTES:
            assert v == result_layer[k]
        else:
            assert k not in result_layer
