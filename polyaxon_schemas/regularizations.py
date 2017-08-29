# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema


class BaseRegularizerSchema(Schema):
    name = fields.Str(allow_none=True)
    collect = fields.Bool(default=True, missing=True)


class BaseRegularizerConfig(BaseConfig):
    def __init__(self, name, collect=True):
        self.name = name
        self.collect = collect


class L1RegularizerSchema(BaseRegularizerSchema):
    l = fields.Float(default=0.01, missing=0.01)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return L1RegularizerConfig(**data)


class L1RegularizerConfig(BaseRegularizerConfig):
    IDENTIFIER = 'L1'
    SCHEMA = L1RegularizerSchema

    def __init__(self, l=0.01, name='L1Regularizer', collect=True):
        self.l = l
        super(L1RegularizerConfig, self).__init__(name, collect)


class L2RegularizerSchema(BaseRegularizerSchema):
    l = fields.Float(default=0.01, missing=0.01)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return L2RegularizerConfig(**data)


class L2RegularizerConfig(BaseRegularizerConfig):
    IDENTIFIER = 'L2'
    SCHEMA = L2RegularizerSchema

    def __init__(self, l=0.01, name='L2Regularizer', collect=True):
        self.l = l
        super(L2RegularizerConfig, self).__init__(name, collect)


class L1L2RegularizerSchema(BaseRegularizerSchema):
    l1 = fields.Float(default=0.01, missing=0.01)
    l2 = fields.Float(default=0.01, missing=0.01)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return L1L2RegularizerConfig(**data)


class L1L2RegularizerConfig(BaseRegularizerConfig):
    IDENTIFIER = 'L1L2'
    SCHEMA = L1L2RegularizerSchema

    def __init__(self, l1=0.01, l2=0.01, name='L1L2Regularizer', collect=True):
        self.l1 = l1
        self.l2 = l2
        super(L1L2RegularizerConfig, self).__init__(name, collect)


class RegularizerSchema(BaseMultiSchema):
    __multi_schema_name__ = 'regularizer'
    __configs__ = {
        L1RegularizerConfig.IDENTIFIER: L1RegularizerConfig,
        L2RegularizerConfig.IDENTIFIER: L2RegularizerConfig,
        L1L2RegularizerConfig.IDENTIFIER: L1L2RegularizerConfig,
    }
    __support_snake_case__ = True
