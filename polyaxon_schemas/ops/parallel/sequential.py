# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.fields.ref_or_obj import RefOrObject


class SequentialSearchSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("sequential"))
    values = RefOrObject(fields.List(fields.Dict(), allow_none=True))

    @staticmethod
    def schema_config():
        return SequentialSearchConfig


class SequentialSearchConfig(BaseConfig):
    SCHEMA = SequentialSearchSchema
    IDENTIFIER = "sequential"

    def __init__(self, values, kind="sequential"):
        self.values = values
        self.kind = kind
