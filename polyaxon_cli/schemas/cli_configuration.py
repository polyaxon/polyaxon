# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.log_handler import LogHandlerSchema


class CliConfigurationSchema(Schema):
    check_count = fields.Int(allow_none=True)
    current_version = fields.Str(allow_none=True)
    min_version = fields.Str(allow_none=True)
    log_handler = fields.Nested(LogHandlerSchema, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return CliConfigurationConfig(**data)

    @post_dump
    def unmake(self, data):
        return CliConfigurationConfig.remove_reduced_attrs(data)


class CliConfigurationConfig(BaseConfig):
    SCHEMA = CliConfigurationSchema
    IDENTIFIER = 'cli'

    def __init__(self, check_count=0, current_version=None, min_version=None, log_handler=None):
        self.check_count = check_count
        self.current_version = current_version
        self.min_version = min_version
        self.log_handler = log_handler
