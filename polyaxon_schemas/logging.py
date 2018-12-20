# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.base import BaseConfig, BaseSchema


class LoggingSchema(BaseSchema):
    level = fields.Str(allow_none=True, validate=validate.OneOf(
        ['INFO', 'DEBUG', 'WARN', 'ERROR', 'FATAL']))
    formatter = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return LoggingConfig


class LoggingConfig(BaseConfig):
    SCHEMA = LoggingSchema
    IDENTIFIER = 'logging'

    def __init__(self, level='INFO', formatter=None):
        self.level = level
        self.formatter = formatter
