# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

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


class GraphConfig(BaseConfig):
    SCHEMA = GraphSchema
    IDENTIFIER = 'graph'

    def __init__(self, input_layers, output_layers, layers, name='graph'):
        self.input_layers = input_layers
        self.output_layers = output_layers
        self.layers = layers
        self.name = name
