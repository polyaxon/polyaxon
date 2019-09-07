# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.ops.parallel.matrix import MatrixSchema
from polyaxon_schemas.ops.parallel.metrics import SearchMetricSchema


class ResourceTypes(object):
    INT = "int"
    FLOAT = "float"

    INT_VALUES = [INT, INT.upper(), INT.capitalize()]
    FLOAT_VALUES = [FLOAT, FLOAT.upper(), FLOAT.capitalize()]

    VALUES = INT_VALUES + FLOAT_VALUES

    @classmethod
    def is_int(cls, value):
        return value in cls.INT_VALUES

    @classmethod
    def is_float(cls, value):
        return value in cls.FLOAT_VALUES


class ResourceSchema(BaseSchema):
    name = fields.Str()
    type = fields.Str(allow_none=True, validate=validate.OneOf(ResourceTypes.VALUES))

    @staticmethod
    def schema_config():
        return ResourceConfig


class ResourceConfig(BaseConfig):
    SCHEMA = ResourceSchema
    IDENTIFIER = "resource"

    def __init__(self, name, type=ResourceTypes.FLOAT):  # noqa, redefined-builtin `len`
        self.name = name
        self.type = type

    def cast_value(self, value):
        if ResourceTypes.is_int(self.type):
            return int(value)
        if ResourceTypes.is_float(self.type):
            return float(value)
        return value


class HyperbandSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("hyperband"))
    matrix = fields.Dict(
        keys=fields.Str(), values=fields.Nested(MatrixSchema), allow_none=True
    )
    max_iter = fields.Int(validate=validate.Range(min=1))
    eta = fields.Float(validate=validate.Range(min=0))
    resource = fields.Nested(ResourceSchema)
    metric = fields.Nested(SearchMetricSchema)
    resume = fields.Boolean(allow_none=True)
    seed = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return HyperbandConfig


class HyperbandConfig(BaseConfig):
    SCHEMA = HyperbandSchema
    IDENTIFIER = "hyperband"

    def __init__(
        self, matrix, max_iter, eta, resource, metric, resume=False, seed=None, kind="hyperband"
    ):
        self.matrix = matrix
        self.kind = kind
        self.max_iter = max_iter
        self.eta = eta
        self.resource = resource
        self.metric = metric
        self.seed = seed
        self.resume = resume
