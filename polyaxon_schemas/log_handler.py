# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig


class LogHandlerSchema(Schema):
    dns = fields.Str()
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

    def __init__(self, dns, environment, tags):
        self.dns = dns
        self.environment = environment
        self.tags = tags
