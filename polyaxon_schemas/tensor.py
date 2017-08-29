# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields

from polyaxon_schemas.base import BaseConfig


class BaseLossSchema(Schema):
    name = fields.Str()
    node = fields.Int(allow_none=True)
    index = fields.Int(allow_none=True)


class BaseLossConfig(BaseConfig):
    def __init__(self, input_layer=None, output_layer=None, weights=1.0, name=None, collect=True):
        self.input_layer = input_layer
        self.output_layer = output_layer
        self.weights = weights
        self.name = name
        self.collect = collect
