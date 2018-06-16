# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import base64

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig


class LogHandlerSchema(Schema):
    dns = fields.Str(allow_none=True)
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

    def __init__(self, environment, tags, dns=None):
        self.dns = dns
        self.environment = environment
        self.tags = tags

    @property
    def decoded_dns(self):
        if self.dns:
            return base64.b64decode(self.dns.encode('utf-8')).decode('utf-8')
