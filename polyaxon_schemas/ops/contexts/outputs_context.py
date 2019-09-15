# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema


class OutputsContextSchema(BaseSchema):
    enabled = fields.Bool(allow_none=True)
    managed = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return OutputsContextConfig


class OutputsContextConfig(BaseConfig):
    IDENTIFIER = "outputs_context"
    SCHEMA = OutputsContextSchema
    REDUCED_ATTRIBUTES = ["enabled", "managed"]

    def __init__(self, enabled=None, managed=None):
        self.enabled = enabled
        self.managed = managed
