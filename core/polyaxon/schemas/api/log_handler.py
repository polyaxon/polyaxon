#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64

from marshmallow import fields

from polyaxon.schemas.base import BaseConfig, BaseSchema


class LogHandlerSchema(BaseSchema):
    dsn = fields.Str(allow_none=True)
    environment = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return LogHandlerConfig


class LogHandlerConfig(BaseConfig):
    SCHEMA = LogHandlerSchema
    IDENTIFIER = "log_handler"

    def __init__(self, dsn=None, environment=None):
        self.dsn = dsn
        self.environment = environment

    @property
    def decoded_dsn(self):
        if self.dsn:
            return base64.b64decode(self.dsn.encode("utf-8")).decode("utf-8")
