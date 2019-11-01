#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon.schemas.base import BaseConfig, BaseSchema


class EmailSchema(BaseSchema):
    host = fields.Str(allow_none=True)
    port = fields.Int(allow_none=True)
    useTls = fields.Bool(allow_none=True)
    hostUser = fields.Str(allow_none=True)
    hostPassword = fields.Str(allow_none=True)
    backend = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return EmailConfig


class EmailConfig(BaseConfig):
    SCHEMA = EmailSchema
    REDUCED_ATTRIBUTES = [
        "host",
        "port",
        "useTls",
        "hostUser",
        "hostPassword",
        "backend",
    ]

    def __init__(
        self,  # noqa
        host=None,
        port=None,
        useTls=None,
        hostUser=None,
        hostPassword=None,
        backend=None,
    ):
        self.host = host
        self.port = port
        self.useTls = useTls
        self.hostUser = hostUser
        self.hostPassword = hostPassword
        self.backend = backend
