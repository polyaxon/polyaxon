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

from marshmallow import fields

from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class EmailSchema(BaseCamelSchema):
    enabled = fields.Bool(allow_none=True)
    email_from = fields.Str(allow_none=True, data_key="from")
    host = fields.Str(allow_none=True)
    port = fields.Int(allow_none=True)
    use_tls = fields.Bool(allow_none=True)
    host_user = fields.Str(allow_none=True)
    host_password = fields.Str(allow_none=True)
    backend = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return EmailConfig


class EmailConfig(BaseConfig):
    SCHEMA = EmailSchema
    REDUCED_ATTRIBUTES = [
        "enabled",
        "from",
        "host",
        "port",
        "useTls",
        "hostUser",
        "hostPassword",
        "backend",
    ]

    def __init__(
        self,  # noqa
        enabled=None,
        email_from=None,
        host=None,
        port=None,
        use_tls=None,
        host_user=None,
        host_password=None,
        backend=None,
    ):
        self.enabled = enabled
        self.email_from = email_from
        self.host = host
        self.port = port
        self.use_tls = use_tls
        self.host_user = host_user
        self.host_password = host_password
        self.backend = backend
