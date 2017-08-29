# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema


class MaxNormSchema(Schema):
    max_value = fields.Int(default=2, missing=2)
    axis = fields.Int(default=0, missing=0)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MaxNormConfig(**data)


class MaxNormConfig(BaseConfig):
    IDENTIFIER = 'MaxNorm'
    SCHEMA = MaxNormSchema

    def __init__(self, max_value=2, axis=0):
        self.max_value = max_value
        self.axis = axis


class NonNegSchema(Schema):
    w = fields.Float()

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return NonNegConfig(**data)


class NonNegConfig(BaseConfig):
    IDENTIFIER = 'NonNeg'
    SCHEMA = NonNegSchema

    def __init__(self, w):
        self.w = w


class UnitNormSchema(Schema):
    axis = fields.Int(default=0, missing=0)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return UnitNormConfig(**data)


class UnitNormConfig(BaseConfig):
    IDENTIFIER = 'UnitNorm'
    SCHEMA = UnitNormSchema

    def __init__(self, axis=0):
        self.axis = axis


class MinMaxNormSchema(Schema):
    min_value = fields.Float(default=0., missing=0.)
    max_value = fields.Float(default=1., missing=1.)
    rate = fields.Float(default=1., missing=1.)
    axis = fields.Int(default=0, missing=0)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MinMaxNormConfig(**data)


class MinMaxNormConfig(BaseConfig):
    IDENTIFIER = 'MinMaxNorm'
    SCHEMA = MinMaxNormSchema

    def __init__(self, min_value=0.0, max_value=1.0, rate=1.0, axis=0):
        self.min_value = min_value
        self.max_value = max_value
        self.rate = rate
        self.axis = axis


class ConstraintSchema(BaseMultiSchema):
    __multi_schema_name__ = 'constraint'
    __configs__ = {
        MaxNormConfig.IDENTIFIER: MaxNormConfig,
        NonNegConfig.IDENTIFIER: NonNegConfig,
        UnitNormConfig.IDENTIFIER: UnitNormConfig,
        MinMaxNormConfig.IDENTIFIER: MinMaxNormConfig,
    }
