# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate, validates_schema

from polyaxon_schemas.base import BaseConfig, BaseSchema


class SequentialSearchSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("sequential"))
    values = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return SequentialSearchConfig


class SequentialSearchConfig(BaseConfig):
    SCHEMA = SequentialSearchSchema
    IDENTIFIER = "sequential"

    def __init__(self, values, kind="sequential"):
        self.values = values
        self.kind = kind
