# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.utils import DType, ObjectOrListObject, Tensor, get_value


class BaseLayerSchema(Schema):
    name = fields.Str(allow_none=True)
    trainable = fields.Bool(default=True, missing=True)
    dtype = DType(allow_none=True)
    inbound_nodes = ObjectOrListObject(Tensor, allow_none=True)

    def get_attribute(self, attr, obj, default):
        return get_value(attr, obj, default)


class BaseLayerConfig(BaseConfig):
    REDUCED_ATTRIBUTES = ['name']

    def __init__(self, name=None, trainable=True, dtype='float32', inbound_nodes=None):
        self.name = name
        self.trainable = trainable
        self.dtype = dtype
        self.inbound_nodes = inbound_nodes or []
