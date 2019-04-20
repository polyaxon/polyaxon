# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_cli.schemas import BaseConfig, BaseSchema, LogHandlerSchema


class CliConfigurationSchema(BaseSchema):
    check_count = fields.Int(allow_none=True)
    current_version = fields.Str(allow_none=True)
    min_version = fields.Str(allow_none=True)
    log_handler = fields.Nested(LogHandlerSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return CliConfigurationConfig


class CliConfigurationConfig(BaseConfig):
    SCHEMA = CliConfigurationSchema
    IDENTIFIER = 'cli'

    def __init__(self, check_count=0, current_version=None, min_version=None, log_handler=None):
        self.check_count = check_count
        self.current_version = current_version
        self.min_version = min_version
        self.log_handler = log_handler
