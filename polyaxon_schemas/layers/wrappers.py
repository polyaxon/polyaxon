# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, post_load

from polyaxon_schemas.layers.base import BaseLayerSchema, BaseLayerConfig


class WrapperSchema(BaseLayerSchema):
    layer = fields.Nested('LayerSchema')

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return WrapperConfig(**data)


class WrapperConfig(BaseLayerConfig):
    IDENTIFIER = 'Wrapper'
    SCHEMA = WrapperSchema

    def __init__(self, layer, **kwargs):
        super(WrapperConfig, self).__init__(**kwargs)
        self.layer = layer


class TimeDistributedSchema(WrapperSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return TimeDistributedConfig(**data)


class TimeDistributedConfig(WrapperConfig):
    IDENTIFIER = 'TimeDistributed'
    SCHEMA = TimeDistributedSchema


class BidirectionalSchema(WrapperSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return BidirectionalConfig(**data)


class BidirectionalConfig(WrapperConfig):
    IDENTIFIER = 'Bidirectional'
    SCHEMA = BidirectionalSchema
