# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_cli.schemas import BaseConfig, BaseSchema


class GlobalConfigurationSchema(BaseSchema):
    verbose = fields.Bool(allow_none=True)
    host = fields.Str(allow_none=True)
    port = fields.Str(allow_none=True)
    use_https = fields.Bool(allow_none=True)
    verify_ssl = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return GlobalConfigurationConfig


class GlobalConfigurationConfig(BaseConfig):
    SCHEMA = GlobalConfigurationSchema
    IDENTIFIER = 'global'

    def __init__(self,
                 verbose=False,
                 host='localhost',
                 port=80,
                 use_https=False,
                 verify_ssl=None):
        self.verbose = verbose
        self.host = host
        self.port = str(port)
        self.use_https = use_https
        self.verify_ssl = verify_ssl
