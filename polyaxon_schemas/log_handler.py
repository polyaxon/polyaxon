# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import base64

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig


class LogHandlerSchema(Schema):
    dsn = fields.Str(allow_none=True)
    environment = fields.Str()
    tags = fields.Dict()

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return LogHandlerConfig(**data)

    @post_dump
    def unmake(self, data):
        return LogHandlerConfig.remove_reduced_attrs(data)


class LogHandlerConfig(BaseConfig):
    SCHEMA = LogHandlerSchema
    IDENTIFIER = 'log_handler'

    def __init__(self, environment, tags, dsn=None):
        self.dsn = dsn
        self.environment = environment
        self.tags = tags

    @property
    def decoded_dsn(self):
        if self.dsn:
            return base64.b64decode(self.dsn.encode('utf-8')).decode('utf-8')
