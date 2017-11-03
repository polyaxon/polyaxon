# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

import six

try:
    from tensorflow.python.keras._impl.keras.backend import set_learning_phase
    from tensorflow.python.keras._impl.keras.engine.topology import Container, InputLayer
except ImportError:
    from tensorflow.contrib.keras.python.keras.backend import set_learning_phase
    from tensorflow.contrib.keras.python.keras.engine.topology import Container, InputLayer

from polyaxon_schemas.graph import GraphConfig

from polyaxon import Modes
from polyaxon.layers import LAYERS
from polyaxon.libs.exceptions import ConfigurationError
from polyaxon.processing import IMAGE_PROCESSORS


class Graph(Container):
    @staticmethod
    def get_node_data(node):
        if isinstance(node, list):
            if len(node) != 3:
                raise ConfigurationError("Node format is not supported `{}`. "
                                         "Node must be a string or "
                                         "[layer_name, node_index, tensor_index]".format(node))
            return node
        if isinstance(node, six.string_types):
            return [node, 0, 0]
        raise ConfigurationError("Node type `{}` is not supported.".format(type(node)))

    @classmethod
    def from_config(cls, mode, features, labels, config):  # pylint: disable=arguments-differ
        """Instantiates a Graph container from its config (output of `get_config()`).

        Arguments:
            mode:
            features:
            labels:
            config: Model config dictionary.

        Returns:
            A model instance.

        Raises:
            ValueError: In case of improperly formatted config dict.
        """
        # set the training mode
        set_learning_phase(Modes.is_train(mode))

        if not isinstance(config, GraphConfig):
            config = GraphConfig.from_dict(config)

        # layer instances created during
        # the graph reconstruction process
        created_layers = {}

        # Create an input layer based on the defined inputs and features
        for layer in config.input_layers:
            layer_name, node_index, tensor_index = cls.get_node_data(layer)
            if layer_name in features:
                created_layers[layer_name] = InputLayer(
                    input_tensor=features[layer_name], name=layer_name)
            elif isinstance(labels, Mapping) and layer_name in labels:
                created_layers[layer_name] = InputLayer(
                    input_tensor=labels[layer_name], name=layer_name)
            else:
                raise ConfigurationError("Input `{}`is not found".format(layer_name))

        def process_layer(layer):
            """Deserialize a layer, then call it on appropriate inputs.

            Arguments:
                layer_data: layer config dict.

            Raises:
                ValueError: In case of improperly formatted `layer_data` dict.
            """
            layer_class = layer.IDENTIFIER
            layer_name = layer.name

            # Instantiate layer.
            if layer_class in LAYERS:
                created_layer = LAYERS[layer_class].from_config(layer)
            elif layer_class in IMAGE_PROCESSORS:
                created_layer = IMAGE_PROCESSORS[layer_class].from_config(layer)
            else:
                raise ValueError("The layer `{}` is not supported.".format(layer_class))
            created_layers[layer_name] = created_layer

            # Gather layer inputs.
            inbound_nodes_data = layer.inbound_nodes
            input_tensors = []
            for input_data in inbound_nodes_data:
                in_layer_name, in_node_index, in_tensor_index = cls.get_node_data(input_data)
                if len(input_data) == 3:
                    kwargs = {}
                elif len(input_data) == 4:
                    kwargs = input_data[3]
                else:
                    raise ValueError('Improperly formatted model config.')
                if in_layer_name not in created_layers:
                    raise ValueError('Missing layer: ' + in_layer_name)
                inbound_layer = created_layers[in_layer_name]
                inbound_node = inbound_layer.inbound_nodes[in_node_index]
                input_tensors.append(inbound_node.output_tensors[in_tensor_index])
            # Call layer on its inputs, thus creating the node
            # and building the layer if needed.
            if input_tensors:
                if len(input_tensors) == 1:
                    created_layer(input_tensors[0], **kwargs)
                else:
                    created_layer(input_tensors, **kwargs)

        for layer in config.layers:
            process_layer(layer)

        name = config.name
        input_tensors = []
        output_tensors = []
        for layer_data in config.input_layers:
            layer_name, node_index, tensor_index = cls.get_node_data(layer_data)
            assert layer_name in created_layers, "Layer `{}` not found".format(layer_name)
            layer = created_layers[layer_name]
            layer_output_tensors = layer.inbound_nodes[node_index].output_tensors
            input_tensors.append(layer_output_tensors[tensor_index])
        for layer_data in config.output_layers:
            layer_name, node_index, tensor_index = cls.get_node_data(layer_data)
            assert layer_name in created_layers
            layer = created_layers[layer_name]
            layer_output_tensors = layer.inbound_nodes[node_index].output_tensors
            output_tensors.append(layer_output_tensors[tensor_index])
        return cls(inputs=input_tensors, outputs=output_tensors, name=name)
