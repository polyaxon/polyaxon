# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_cli.schemas.base import BaseConfig, BaseSchema


class GlobalConfigurationSchema(BaseSchema):
    verbose = fields.Bool(allow_none=True)
    host = fields.Str(allow_none=True)
    http_port = fields.Str(allow_none=True)
    ws_port = fields.Str(allow_none=True)
    use_https = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return GlobalConfigurationConfig


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
