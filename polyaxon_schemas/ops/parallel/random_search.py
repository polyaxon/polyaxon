# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.fields.ref_or_obj import RefOrObject
from polyaxon_schemas.ops.parallel.matrix import MatrixSchema


class RandomSearchSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("random"))
    matrix = fields.Dict(
        keys=fields.Str(), values=fields.Nested(MatrixSchema), allow_none=True
    )
    n_experiments = RefOrObject(
        fields.Int(allow_none=True, validate=validate.Range(min=1))
    )
    seed = RefOrObject(fields.Int(allow_none=True))

    @staticmethod
    def schema_config():
        return RandomSearchConfig


class RandomSearchConfig(BaseConfig):
    SCHEMA = RandomSearchSchema
    IDENTIFIER = "random"
    REDUCED_ATTRIBUTES = ["seed", "n_experiments"]

    def __init__(self, matrix, n_experiments=None, seed=None, kind="random"):
        self.matrix = matrix
        self.kind = kind
        self.n_experiments = n_experiments
        self.seed = seed
