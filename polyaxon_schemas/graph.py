# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.layers import LayerSchema
from polyaxon_schemas.utils import ObjectOrListObject, Tensor


class GraphSchema(Schema):
    input_layers = ObjectOrListObject(Tensor)
    output_layers = ObjectOrListObject(Tensor)
    layers = fields.Nested(LayerSchema, many=True)
    name = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return GraphConfig(**data)

    @post_dump
    def unmake(self, data):
        return GraphConfig.remove_reduced_attrs(data)


class GraphConfig(BaseConfig):
    """A Graph is a directed acyclic graph of layers.

    It is the topological form for creating a computational graph.
    The graph contains a list of layers/tensor operations, i.e.

    ```yaml
    - layer_name:
        arg1: value
        arg2: value
    - layer_name:
        arg1: value
        arg2: value
    ```

    The graph must define its inputs, i.e. `input_layers`,
    usually the names of the tensors that these graph is expecting from a preprocessing step.

    ```yaml
    graph:
      input_layers: ['input1', 'input2']
      layers:
        - layer_name:
        ...
    ```

    A graph can also specify the outputs, i.e. `output_layers`,
    when not specified, the `output_layers` will contain by default the last layer.
    when specified, if the `output_layers` do not contain the last layer it will be added.

    ```yaml
    graph:
      input_layers: ['image']
      layers:
        - Dense:
          units: 2
        - Dense:
          units: 2
          name: last_layer
    ```

    This is equivalent to

    ```yaml
    graph:
      input_layers: [image]
      layers:
        - Dense:
          units: 2
        - Dense:
          units: 2
          name: last_layer
      output_layers: [last_layer]
    ```

    Defining multiple outputs could be achieved in different ways,
    either by listing all `output_layers` or by using the `is_output: True` on the specific layer.

    ```yaml
    graph:
      input_layers: [image]
      layers:
        - Dense:
          units: 2
          is_output: true
        - Dense:
          units: 2
          name: last_layer
      output_layers: [last_layer]
    ```

    Means that, both `last_layer` and `dense_1` are in the list of the `output_layers`.

    This is the same as

    ```yaml
    graph:
      input_layers: [image]
      layers:
        - Dense:
          units: 2
        - Dense:
          units: 2
          name: last_layer
      output_layers: [dense_1, last_layer]
    ```

    A graph can optionally have a name

    ```yaml
    graph:
      name: cool_graph
      input_layers: [image]
      layers:
        - ...
    ```

    Args:
        name: the name of the graph
        input_layers: `str` or `list` of `str`, the input layers for the graph.
        output_layers: `str` or `list` of `str`, the output layers for the graph.
        layers: `list`, list of layers.

    Polyaxonfile usage:

    ```yaml
    graph:
      input_layers: image
      layers:
        - Dense:
            units: 128
        - Dense:
            units: 256
            name: dense_out
    ```

    or

    ```yaml
    graph:
      input_layers: image
      layers:
        - Dense:
            units: 128
        - Dense:
            units: 256
            name: dense_out
      output_layers: dense_out
    ```
    """
    SCHEMA = GraphSchema
    IDENTIFIER = 'graph'
    REDUCED_ATTRIBUTES = ['name']

    def __init__(self, input_layers, output_layers, layers, name='graph'):
        self.input_layers = input_layers
        self.output_layers = output_layers
        self.layers = layers
        self.name = name
