# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import base64

from marshmallow import fields

from polyaxon.schemas.base import BaseConfig, BaseSchema


class LogHandlerSchema(BaseSchema):
    dsn = fields.Str(allow_none=True)
    environment = fields.Str()

    @staticmethod
    def schema_config():
        return LogHandlerConfig


class LogHandlerConfig(BaseConfig):
    SCHEMA = LogHandlerSchema
    IDENTIFIER = "log_handler"

    def __init__(self, environment, dsn=None):
        self.dsn = dsn
        self.environment = environment

    @property
    def decoded_dsn(self):
        if self.dsn:
            return base64.b64decode(self.dsn.encode("utf-8")).decode("utf-8")
