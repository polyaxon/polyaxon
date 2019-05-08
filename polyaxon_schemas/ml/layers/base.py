# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import EXCLUDE, fields

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.fields import ObjectOrListObject, Tensor
from polyaxon_schemas.ml.fields import DType
from polyaxon_schemas.utils import get_value


class BaseLayerSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    trainable = fields.Bool(default=True, missing=True)
    dtype = DType(allow_none=True)
    inbound_nodes = ObjectOrListObject(Tensor, allow_none=True)

    class Meta:
        unknown = EXCLUDE
        ordered = True

    def get_attribute(self, obj, attr, default):
        return get_value(attr, obj, default)


class BaseLayerConfig(BaseConfig):
    REDUCED_ATTRIBUTES = ['name']
    UNKNOWN_BEHAVIOUR = EXCLUDE

    def __init__(self, name=None, trainable=True, dtype='float32', inbound_nodes=None):
        self.name = name
        self.trainable = trainable
        self.dtype = dtype
        self.inbound_nodes = inbound_nodes or []
