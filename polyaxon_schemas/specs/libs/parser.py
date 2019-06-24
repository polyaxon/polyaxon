# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import ast
import copy
import jinja2
import numpy as np
import six

from collections import Mapping, defaultdict

from hestia.list_utils import to_list
from rhea.utils import deep_update

from polyaxon_schemas.exceptions import PolyaxonfileError


class Parser(object):
    """Parses the Polyaxonfile."""

    env = jinja2.Environment()

    @classmethod
    def get_headers(cls, spec, data):
        parsed_data = {
            section: data[section] for section in spec.HEADER_SECTIONS
            if data.get(section)
        }
        return parsed_data

    @staticmethod
    def _get_section(config, section):
        if not hasattr(config, section):
            return None
        section_data = getattr(config, section)
        if hasattr(section_data, 'to_dict'):
            return section_data.to_dict()
        return section_data

    @classmethod
    def parse(cls, spec, config, params, matrix_params=None):  # pylint:disable=too-many-branches
        params = params or {}
        matrix_params = copy.copy(matrix_params)
        if matrix_params:
            params = deep_update(matrix_params, params)

        parsed_data = {
            spec.VERSION: config.version,
            spec.KIND: config.kind,
        }

        if params:
            params = cls.parse_expression(spec, params, params)
            parsed_data[spec.PARAMS] = params

        for section in spec.STD_PARSING_SECTIONS:
            config_section = cls._get_section(config, section)
            if config_section:
                parsed_data[section] = cls.parse_expression(spec, config_section, params)

        for section in spec.OP_PARSING_SECTIONS:
            config_section = cls._get_section(config, section)
            if config_section:
                parsed_data[section] = cls.parse_expression(
                    spec, config_section, params, True, False)

        config_section = cls._get_section(config, spec.RUN)
        if config_section:
            parsed_data[spec.RUN] = cls.parse_expression(spec, config_section, params, True, False)

        for section in spec.GRAPH_SECTIONS:
            config_section = cls._get_section(config, section)
            if config_section:
                parsed_data[section] = cls.parse_expression(
                    spec, config_section, params, True, True)

        return parsed_data

    @classmethod
    def parse_expression(cls,  # pylint:disable=too-many-branches
                         spec,
                         expression,
                         params,
                         check_operators=False,
                         check_graph=False):
        if isinstance(expression, (int, float, complex, type(None))):
            return expression
        if isinstance(expression, np.integer):
            return int(expression)
        if isinstance(expression, np.floating):
            return float(expression)
        if isinstance(expression, Mapping):
            if len(expression) == 1:
                old_key, value = list(six.iteritems(expression))[0]
                # always parse the keys, they must be base object or evaluate to base objects
                key = cls.parse_expression(spec, old_key, params)
                if check_operators and cls.is_operator(spec, key):
                    return cls._parse_operator(spec, {key: value}, params)
                if check_graph and key in ['graph', 'encoder', 'decoder']:
                    return {key: cls._parse_graph(spec, value, params)}
                if check_graph and key == 'feature_processors':  # noqa, no-else-return
                    return {
                        key: {
                            cls.parse_expression(spec, f_key, params):
                                cls._parse_graph(spec, f_vlaue, params)
                            for f_key, f_vlaue in six.iteritems(value)
                        }
                    }
                else:
                    return {
                        key: cls.parse_expression(
                            spec, value, params, check_operators, check_graph)
                    }

            new_expression = {}
            for k, v in six.iteritems(expression):
                new_expression.update(
                    cls.parse_expression(spec, {k: v}, params, check_operators, check_graph))
            return new_expression

        if isinstance(expression, list):
            return list(cls.parse_expression(spec, v, params, check_operators, check_graph)
                        for v in expression)
        if isinstance(expression, tuple):
            return tuple(cls.parse_expression(spec, v, params, check_operators, check_graph)
                         for v in expression)
        if isinstance(expression, six.string_types):
            return cls._evaluate_expression(
                spec, expression, params, check_operators, check_graph)

    @classmethod
    def _evaluate_expression(cls, spec, expression, params, check_operators, check_graph):
        result = cls.env.from_string(expression).render(**params)
        if result == expression:
            try:
                return ast.literal_eval(result)
            except (ValueError, SyntaxError):
                pass
            return result
        return cls.parse_expression(spec, result, params, check_operators, check_graph)

    @classmethod
    def _parse_operator(cls, spec, expression, params):
        k, v = list(six.iteritems(expression))[0]
        op = spec.OPERATORS[k].from_dict(v)
        return op.parse(spec=spec, parser=cls, params=params)

    @staticmethod
    def is_operator(spec, key):
        return key in spec.OPERATORS

    @classmethod
    def _parse_graph(cls, spec, graph, params):  # noqa, too-many-branches
        input_layers = to_list(graph['input_layers'])
        layer_names = set(input_layers)
        tags = {}
        layers = []
        outputs = []
        layers_counters = defaultdict(int)
        unused_layers = set(input_layers)

        if not isinstance(graph['layers'], list):
            raise PolyaxonfileError("Graph definition expects a list of layer definitions.")

        def add_tag(tag, layer_value):
            if tag in tags:
                tags[tag] = to_list(tags[tag])
                tags[tag].append(layer_value['name'])
            else:
                tags[tag] = layer_value['name']

        def get_layer_name(layer_value, layer_type):
            if 'name' not in layer_value:
                layers_counters[layer_type] += 1
                return '{}_{}'.format(layer_type, layers_counters[layer_type])

            return layer_value['name']

        layers_params = {}
        layers_params.update(params)

        last_layer = None
        first_layer = True
        for layer_expression in graph['layers']:
            parsed_layer = cls.parse_expression(spec, layer_expression, layers_params, True)
            # Gather all tags from the layers
            parsed_layer = to_list(parsed_layer)
            for layer in parsed_layer:
                if not layer:
                    continue

                layer_type, layer_value = list(six.iteritems(layer))[0]

                if layer_value is None:
                    layer_value = {}
                # Check that the layer has a name otherwise generate one
                name = get_layer_name(layer_value, layer_type)
                if name not in layer_names:
                    layer_names.add(name)
                    layer_value['name'] = name
                else:
                    raise PolyaxonfileError(
                        "The name `{}` is used 2 times in the graph. "
                        "All layer names should be unique. "
                        "If you need to reference a layer in a for loop "
                        "think about using `tags`".format(name))

                for tag in to_list(layer_value.get('tags', [])):
                    add_tag(tag, layer_value)

                # Check if the layer is an output
                if layer_value.get('is_output', False) is True:
                    outputs.append(layer_value['name'])
                else:
                    # Add the layer to unused
                    unused_layers.add(layer_value['name'])

                # Check the layers inputs
                if not layer_value.get('inbound_nodes'):
                    if last_layer is not None:
                        layer_value['inbound_nodes'] = [
                            last_layer['name']]  # noqa, unsubscriptable-object
                    if first_layer and len(input_layers) == 1:
                        layer_value['inbound_nodes'] = input_layers
                    if first_layer and len(input_layers) > 1:
                        raise PolyaxonfileError("The first layer must indicate which input to use,"
                                                "You have {} layers: {}".format(len(input_layers),
                                                                                input_layers))

                first_layer = False
                for input_layer in layer_value.get('inbound_nodes', []):
                    if input_layer not in layer_names:
                        raise PolyaxonfileError(
                            "The layer `{}` has a non existing "
                            "inbound node `{}`".format(layer_value['name'], input_layer))
                    if input_layer in unused_layers:
                        unused_layers.remove(input_layer)

                # Add layer
                layers.append({layer_type: layer_value})

                # Update layers_params
                layers_params['tags'] = tags

                # Update last_layer
                last_layer = layer_value

        # Add last layer as output
        if last_layer:
            if last_layer['name'] not in outputs:
                outputs.append(last_layer['name'])

            # Remove last layer from unused layers
            if last_layer['name'] in unused_layers:
                unused_layers.remove(last_layer['name'])

        # Check if some layers are unused
        if unused_layers:
            raise PolyaxonfileError(
                "These layers `{}` were declared but are not used.".format(unused_layers))

        return {
            'input_layers': to_list(graph['input_layers']),
            'layers': layers,
            'output_layers': outputs
        }
