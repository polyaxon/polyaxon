# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig


class GlobalConfigurationSchema(Schema):
    verbose = fields.Bool(allow_none=True)
    host = fields.Str(allow_none=True)
    http_port = fields.Str(allow_none=True)
    ws_port = fields.Str(allow_none=True)
    use_https = fields.Bool(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return GlobalConfigurationConfig(**data)

    @post_dump
    def unmake(self, data):
        return GlobalConfigurationConfig.remove_reduced_attrs(data)


class GlobalConfigurationConfig(BaseConfig):
    SCHEMA = GlobalConfigurationSchema
    IDENTIFIER = 'global'

    def __init__(self,
                 verbose=False,
                 host='localhost',
                 http_port=80,
                 ws_port=80,
                 use_https=False):
        self.verbose = verbose
        self.host = host
        self.http_port = str(http_port)
        self.ws_port = str(ws_port)
        self.use_https = use_https
