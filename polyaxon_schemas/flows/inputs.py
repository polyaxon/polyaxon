# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema


class InputSchema(BaseSchema):
    name = fields.Str()
    ref = fields.Str()
    type = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return InputConfig


class InputConfig(BaseConfig):
    SCHEMA = InputSchema
    IDENTIFIER = 'dep'

    def __init__(self, name, ref, type=None):   # pylint:disable=redefined-builtin
        self.name = name
        self.ref = ref
        self.type = type
