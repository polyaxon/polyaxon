# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import ast
import jinja2
import six

from collections import Mapping, defaultdict

from polyaxon_schemas.utils import to_list
from polyaxon_schemas.exceptions import PolyaxonfileError
from polyaxon_schemas.polyaxonfile.specification import Specification


class Parser(object):
    """Parses the Polyaxonfile."""

    env = jinja2.Environment()

    @staticmethod
    def validate_version(data):
        if 'version' not in data:
            raise PolyaxonfileError("The Polyaxonfile version must be specified.")
        if not (Specification.MIN_VERSION <= data['version'] <= Specification.MAX_VERSION):
            raise PolyaxonfileError(
                "The Polyaxonfile's version specified is not supported by your current CLI."
                "Your CLI support Polyaxonfile versions between: {} {}."
                "You can run `polyaxon upgrade` and "
                "check documentation for the specification.".format(
                    Specification.MIN_VERSION, Specification.MAX_VERSION))

    @classmethod
    def parse(cls, data):
        cls.validate_version(data)
        sections = Specification.sections()
        for key in (set(six.iterkeys(data)) - sections):
            raise PolyaxonfileError("Unexpected section `{}` in Polyaxonfile version `{}`."
                                    "Please check the Polyaxonfile specification "
                                    "for this version.".format(key, 'v1'))

        parsed_data = {
            'version': data['version'],
        }

        if 'declarations' in data:
            parsed_data['declarations'] = cls.parse_expression(
                data['declarations'], data['declarations'])

        if 'matrix' in data:
            parsed_data['matrix'] = cls.parse_expression(
                data['matrix'], parsed_data.get('declarations'))

        for section in Specification.SECTIONS:
            if section in data:
                parsed_data[section] = cls.parse_expression(
                    data[section], parsed_data.get('declarations', {}))

        for section in Specification.GRAPH_SECTIONS:
            if section in data:
                parsed_data[section] = cls.parse_expression(
                    data[section], parsed_data.get('declarations', {}), True, True)

        return parsed_data

    @classmethod
    def parse_expression(cls, expression, declarations, check_operators=False, check_graph=False):
        if isinstance(expression, (int, float, complex, type(None))):
            return expression
        if isinstance(expression, Mapping):
            if len(expression) == 1:
                key = list(six.iterkeys(expression))[0]
                if check_operators and cls.is_operator(key):
                    return cls._parse_operator(expression, declarations)
                if check_graph and key == 'graph':
                    return cls._parse_graph(expression, declarations)
                else:
                    return {
                        key: cls.parse_expression(
                            expression[key], declarations, check_operators, check_graph)
                    }

            new_expression = {}
            for k, v in six.iteritems(expression):
                new_expression.update(
                    cls.parse_expression({k: v}, declarations, check_operators, check_graph))
            return new_expression

        if isinstance(expression, list):
            return list(cls.parse_expression(v, declarations, check_operators, check_graph)
                        for v in expression)
        if isinstance(expression, tuple):
            return tuple(cls.parse_expression(v, declarations, check_operators, check_graph)
                         for v in expression)
        if isinstance(expression, six.string_types):
            return cls._evaluate_expression(expression, declarations, check_operators, check_graph)

    @classmethod
    def _evaluate_expression(cls, expression, declarations, check_operators, check_graph):
        result = cls.env.from_string(expression).render(**declarations)
        if result == expression:
            try:
                return ast.literal_eval(result)
            except (ValueError, SyntaxError):
                pass
            return result
        return cls.parse_expression(result, declarations, check_operators, check_graph)

    @classmethod
    def _parse_operator(cls, expression, declarations):
        k, v = list(six.iteritems(expression))[0]
        op = Specification.OPERATORS[k].from_dict(v)
        return op.parse(cls, declarations)

    @staticmethod
    def is_operator(key):
        return key in Specification.OPERATORS

    @classmethod
    def _parse_graph(cls, expression, declarations):
        graph = expression['graph']
        layer_names = set([])
        tags = {}
        layers = []
        outputs = []
        layers_counters = defaultdict(int)
        unused_layers = set([])

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

        layers_declarations = {}
        layers_declarations.update(declarations)

        last_layer = None
        for layer_expression in graph['layers']:
            parsed_layer = cls.parse_expression(layer_expression, layers_declarations, True)
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
                if not layer_value.get('inbound_nodes') and last_layer is not None:
                    layer_value['inbound_nodes'] = [last_layer['name']]
                for input_layer in layer_value.get('inbound_nodes', []):
                    if input_layer not in layer_names:
                        raise PolyaxonfileError(
                            "The layer `{}` has a non existing "
                            "inbound node `{}`".format(layer_value['name'], input_layer))
                    if input_layer in unused_layers:
                        unused_layers.remove(input_layer)

                # Add layer
                layers.append({layer_type: layer_value})

                # Update layers_declarations
                layers_declarations['tags'] = tags

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
            'graph': {
                'input_layers': to_list(graph['input_layers']),
                'layers': layers,
                'output_layers': outputs
            }
        }
