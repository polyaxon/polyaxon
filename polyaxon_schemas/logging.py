# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load, validate, post_dump

from polyaxon_schemas.base import BaseConfig


class LoggingSchema(Schema):
    level = fields.Str(allow_none=True, validate=validate.OneOf(
        ['INFO', 'DEBUG', 'WARN', 'ERROR', 'FATAL']))
    formatter = fields.Str(allow_none=True)
    path = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return LoggingConfig(**data)

    @post_dump
    def unmake(self, data):
        return LoggingConfig.remove_reduced_attrs(data)


class LoggingConfig(BaseConfig):
    SCHEMA = LoggingSchema
    IDENTIFIER = 'logging'

    def __init__(self,
                 level='INFO',
                 formatter=None,
                 path=None):
        self.level = level
        self.formatter = formatter
        self.path = path
