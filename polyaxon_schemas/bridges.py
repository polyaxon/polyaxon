# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema
from polyaxon_schemas.utils import ObjectOrListObject


class BaseBridgeSchema(Schema):
    state_size = ObjectOrListObject(fields.Int, allow_none=True)
    name = fields.Str(allow_none=True)


class BaseBridgeConfig(BaseConfig):
    REDUCED_ATTRIBUTES = ['name']

    def __init__(self, state_size=None, name=None):
        self.state_size = state_size
        self.name = name


class LatentBridgeSchema(BaseBridgeSchema):
    latent_dim = fields.Int(allow_none=True)
    mean = fields.Float(allow_none=True)
    stddev = fields.Float(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return LatentBridgeConfig(**data)


class LatentBridgeConfig(BaseBridgeConfig):
    IDENTIFIER = 'LatentBridge'
    SCHEMA = LatentBridgeSchema

    def __init__(self, latent_dim=1, mean=0., stddev=1., **kwargs):
        super(LatentBridgeConfig, self).__init__(**kwargs)
        self.latent_dim = latent_dim
        self.mean = mean
        self.stddev = stddev


class NoOpBridgeSchema(BaseBridgeSchema):
    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return NoOpBridgeConfig(**data)


class NoOpBridgeConfig(BaseBridgeConfig):
    IDENTIFIER = 'NoOpBridge'
    SCHEMA = NoOpBridgeSchema


class BridgeSchema(BaseMultiSchema):
    __multi_schema_name__ = 'bridge'
    __configs__ = {
        LatentBridgeConfig.IDENTIFIER: LatentBridgeConfig,
        NoOpBridgeConfig.IDENTIFIER: NoOpBridgeConfig,
    }
