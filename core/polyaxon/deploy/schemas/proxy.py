#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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


class ProxySchema(BaseCamelSchema):
    enabled = fields.Bool(allow_none=True)
    use_in_ops = fields.Bool(allow_none=True)
    http_proxy = fields.Str(allow_none=True)
    https_proxy = fields.Str(allow_none=True)
    no_proxy = fields.Str(allow_none=True)
    port = fields.Int(allow_none=True)
    host = fields.Str(allow_none=True)
    kind = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return ProxyConfig


class ProxyConfig(BaseConfig):
    SCHEMA = ProxySchema
    REDUCED_ATTRIBUTES = [
        "enabled",
        "useInOps",
        "httpProxy",
        "httpsProxy",
        "noProxy",
        "port",
        "host",
        "kind",
    ]

    def __init__(
        self,
        enabled=None,
        use_in_ops=None,
        http_proxy=None,
        https_proxy=None,
        no_proxy=None,
        port=None,
        host=None,
        kind=None,
    ):
        self.enabled = enabled
        self.use_in_ops = use_in_ops
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy
        self.no_proxy = no_proxy
        self.port = port
        self.host = host
        self.kind = kind
