# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema


class ExecutableSchema(BaseSchema):
    execute_at = fields.LocalDateTime(allow_none=True)
    timeout = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return ExecutableConfig


class ExecutableConfig(BaseConfig):
    SCHEMA = ExecutableSchema
    IDENTIFIER = 'executable'
    REDUCED_ATTRIBUTES = ['execute_at', 'timeout']

    def __init__(self, execute_at=None, timeout=None):
        self.execute_at = execute_at
        self.timeout = timeout
