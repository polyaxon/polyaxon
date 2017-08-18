# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

from polyaxon_schemas.base import BaseConfig


class GlobalConfigurationSchema(Schema):
    verbose = fields.Bool(allow_none=True)
    host = fields.Str(allow_none=True)
    working_directory = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return GlobalConfigurationConfig(**data)


class GlobalConfigurationConfig(BaseConfig):
    SCHEMA = GlobalConfigurationSchema
    IDENTIFIER = 'global'

    def __init__(self, verbose=False, host='localhost', working_directory='.'):
        self.verbose = verbose
        self.host = host
        self.working_directory = working_directory
