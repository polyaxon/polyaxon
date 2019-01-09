# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields
from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema


class EmailSchema(BaseSchema):
    host = fields.Str(allow_none=True)
    port = fields.Int(allow_none=True)
    useTls = fields.Bool(allow_none=True)
    hostUser = fields.Str(allow_none=True)
    hostPassword = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return EmailConfig


class EmailConfig(BaseConfig):
    SCHEMA = EmailSchema
    REDUCED_ATTRIBUTES = ['host', 'port', 'useTls', 'hostUser', 'hostPassword']

    def __init__(self, host=None, port=None, useTls=None, hostUser=None, hostPassword=None):  # noqa
        self.host = host
        self.port = port
        self.useTls = useTls
        self.hostUser = hostUser
        self.hostPassword = hostPassword
