# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_schemas.exceptions import PolyaxonfileError
from polyaxon_schemas.specs import ExperimentSpecification
from polyaxon_schemas.specs.libs.parser import Parser


class TestParser(TestCase):
    def test_parse_base_expressions(self):
        data = [
            1, 10., [1, 1], (1, 1), 'string', ['str1', 'str2'], {1: 2, 'a': 'a', 'dict': {1: 1}}
        ]

        parser = Parser()
        for d in data:
            assert d == parser.parse_expression(ExperimentSpecification, d, {})

    def test_parse_context_expression(self):
        parser = Parser()
        assert parser.parse_expression(ExperimentSpecification, '{{ something }}', {}) == ''
        assert parser.parse_expression(ExperimentSpecification, '{{ something }}',
                                       {'something': 1}) == 1

    def test_parse_graph_expression(self):
        expression = {
            'graph': {
                'input_layers': ['images'],
                'layers': [
                    {'Conv2D': {
                        'filters': 64,
                        'kernel_size': [3, 3],
                        'strides': [1, 1],
                        'activation': 'relu',
                    }},
                    {'MaxPooling2D': {'kernels': 2}},
                    {'Flatten': None},
                    {'Dense': {
                        'units': 10,
                        'activation': 'softmax',
                    }}
                ]
            }
        }

        parser = Parser()
        assert parser.parse_expression(ExperimentSpecification, expression, {}) == expression

        expected_expression = {
            'graph': {'input_layers': ['images'],
                      'layers': [
                          {'Conv2D': {'activation': 'relu',
                                      'filters': 64,
                                      'kernel_size': [3, 3],
                                      'name': 'Conv2D_1',
                                      'strides': [1, 1],
                                      'inbound_nodes': ['images']}
                           },
                          {'MaxPooling2D': {'inbound_nodes': ['Conv2D_1'],
                                            'kernels': 2,
                                            'name': 'MaxPooling2D_1'}
                           },
                          {'Flatten': {'inbound_nodes': ['MaxPooling2D_1'],
                                       'name': 'Flatten_1'}
                           },
                          {'Dense': {'activation': 'softmax',
                                     'inbound_nodes': ['Flatten_1'],
                                     'name': 'Dense_1',
                                     'units': 10}
                           }
                      ],
                      'output_layers': ['Dense_1']}
        }
        assert parser.parse_expression(
            ExperimentSpecification, expression, {}, check_graph=True) == expected_expression

    def test_parse_graph_with_operators_and_tags(self):
        params = {
            'conv2d':
                {
                    'filters': [32, 64],
                    'kernel_size': [[3, 3], [2, 2]],
                    'strides': [1, 1],
                    'activation': ['relu', 'linear']
                }
        }
        expression = {
            'graph': {
                'input_layers': ['images'],
                'layers': [
                    {'for': {
                        'len': 2,
                        'index': 'i',
                        'do':
                            {'Conv2D': {
                                'filters': '{{ conv2d.filters[i] }}',
                                'kernel_size': '{{ conv2d.kernel_size[i] }}',
                                'strides': '{{ conv2d.strides }}',
                                'activation': '{{ conv2d.activation[i] }}',
                                'tags': ['tag1', 'tag2']
                            }}
                    }},
                    {'MaxPooling2D': {'kernels': 2}},
                    {'Flatten': {'name': 'Flatten_1'}},
                    {'Flatten': {'inbound_nodes': ['{{ tags.tag1[0] }}'], 'name': 'Flatten_2'}},
                    {'Concat': {'inbound_nodes': ['Flatten_1', 'Flatten_2']}},
                    {'Dense': {
                        'units': 10,
                        'activation': 'softmax',
                    }}
                ]
            }
        }

        parser = Parser()
        result_expression = parser.parse_expression(
            ExperimentSpecification,
            expression,
            params,
            check_operators=True,
            check_graph=True)
        expected_result = {'graph': {
            'input_layers': ['images'],
            'layers': [
                {'Conv2D': {'activation': 'relu',
                            'filters': 32,
                            'kernel_size': [3, 3],
                            'name': 'Conv2D_1',
                            'strides': [1, 1],
                            'inbound_nodes': ['images'],
                            'tags': ['tag1', 'tag2']}},
                {'Conv2D': {'activation': 'linear',
                            'filters': 64,
                            'inbound_nodes': ['Conv2D_1'],
                            'kernel_size': [2, 2],
                            'name': 'Conv2D_2',
                            'strides': [1, 1],
                            'tags': ['tag1', 'tag2']}},
                {'MaxPooling2D': {'inbound_nodes': ['Conv2D_2'],
                                  'kernels': 2,
                                  'name': 'MaxPooling2D_1'}},
                {'Flatten': {'inbound_nodes': ['MaxPooling2D_1'],
                             'name': 'Flatten_1'}},
                {'Flatten': {'inbound_nodes': ['Conv2D_1'],
                             'name': 'Flatten_2'}},
                {'Concat': {
                    'inbound_nodes': ['Flatten_1', 'Flatten_2'],
                    'name': 'Concat_1'}},
                {'Dense': {'activation': 'softmax',
                           'inbound_nodes': ['Concat_1'],
                           'name': 'Dense_1',
                           'units': 10}}],
            'output_layers': ['Dense_1']}}
        assert result_expression == expected_result

    def test_parse_graph_with_many_inputs_used(self):
        expression = {
            'graph': {
                'input_layers': ['images'],
                'layers': [
                    {'Conv2D': {
                        'filters': 64,
                        'kernel_size': [3, 3],
                        'strides': [1, 1],
                        'activation': 'relu',
                        'inbound_nodes': ['images']
                    }},
                    {'MaxPooling2D': {'kernels': 2}},
                    {'Flatten': None},
                    {'Dense': {
                        'units': 10,
                        'activation': 'softmax',
                    }}
                ]
            }
        }

        parser = Parser()
        assert parser.parse_expression(ExperimentSpecification, expression, {}) == expression

        expected_expression = {
            'graph': {
                'input_layers': ['images'],
                'layers': [
                    {'Conv2D': {'activation': 'relu',
                                'filters': 64,
                                'kernel_size': [3, 3],
                                'name': 'Conv2D_1',
                                'strides': [1, 1],
                                'inbound_nodes': ['images']}
                     },
                    {'MaxPooling2D': {'inbound_nodes': ['Conv2D_1'],
                                      'kernels': 2,
                                      'name': 'MaxPooling2D_1'}
                     },
                    {'Flatten': {'inbound_nodes': ['MaxPooling2D_1'],
                                 'name': 'Flatten_1'}
                     },
                    {'Dense': {'activation': 'softmax',
                               'inbound_nodes': ['Flatten_1'],
                               'name': 'Dense_1',
                               'units': 10}
                     }
                ],
                'output_layers': ['Dense_1']}
        }
        assert parser.parse_expression(
            ExperimentSpecification, expression, {}, check_graph=True) == expected_expression

    def test_parse_graph_with_many_inputs_and_non_used_raises(self):
        expression = {
            'graph': {
                'input_layers': ['images', 'sounds'],
                'layers': [
                    {'Conv2D': {
                        'filters': 64,
                        'kernel_size': [3, 3],
                        'strides': [1, 1],
                        'activation': 'relu',
                        'name': 'Conv2D_1',
                        'inbound_nodes': ['images']
                    }},
                    {'MaxPooling2D': {'kernels': 2}},  # This layer is orphan
                    {'Flatten': {'inbound_nodes': ['Conv2D_1']}},  # Specify the input layer
                    {'Dense': {
                        'units': 10,
                        'activation': 'softmax',
                    }}
                ]
            }
        }

        parser = Parser()
        with self.assertRaises(PolyaxonfileError):
            parser.parse_expression(ExperimentSpecification, expression, {}, check_graph=True)

    def test_parse_graph_with_many_inputs_and_some_used_raises(self):
        expression = {
            'graph': {
                'input_layers': ['images', 'sounds'],
                'layers': [
                    {'Conv2D': {
                        'filters': 64,
                        'kernel_size': [3, 3],
                        'strides': [1, 1],
                        'activation': 'relu',
                        'name': 'Conv2D_1'
                    }},
                    {'MaxPooling2D': {'kernels': 2}},  # This layer is orphan
                    {'Flatten': {'inbound_nodes': ['Conv2D_1']}},  # Specify the input layer
                    {'Dense': {
                        'units': 10,
                        'activation': 'softmax',
                    }}
                ]
            }
        }

        parser = Parser()
        with self.assertRaises(PolyaxonfileError):
            parser.parse_expression(ExperimentSpecification, expression, {}, check_graph=True)

    def test_parse_graph_with_orphan_layers_raises(self):
        expression = {
            'graph': {
                'input_layers': ['images'],
                'layers': [
                    {'Conv2D': {
                        'filters': 64,
                        'kernel_size': [3, 3],
                        'strides': [1, 1],
                        'activation': 'relu',
                        'name': 'Conv2D_1'
                    }},
                    {'MaxPooling2D': {'kernels': 2}},  # This layer is orphan
                    {'Flatten': {'inbound_nodes': ['Conv2D_1']}},  # Specify the input layer
                    {'Dense': {
                        'units': 10,
                        'activation': 'softmax',
                    }}
                ]
            }
        }

        parser = Parser()
        with self.assertRaises(PolyaxonfileError):
            parser.parse_expression(ExperimentSpecification, expression, {}, check_graph=True)
