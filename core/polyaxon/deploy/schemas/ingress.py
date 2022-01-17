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

from marshmallow import INCLUDE, fields

from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class IngressSchema(BaseCamelSchema):
    enabled = fields.Bool(allow_none=True)
    host_name = fields.Str(allow_none=True)
    path = fields.Str(allow_none=True)
    tls = fields.List(fields.Dict(allow_none=True), allow_none=True)
    annotations = fields.Dict(allow_none=True)

    class Meta:
        unknown = INCLUDE

    @staticmethod
    def schema_config():
        return IngressConfig


class IngressConfig(BaseConfig):
    SCHEMA = IngressSchema
    REDUCED_ATTRIBUTES = ["enabled", "hostName", "tls", "annotations", "path"]

    def __init__(
        self,
        enabled=None,
        host_name=None,
        path=None,
        tls=None,
        annotations=None,
        **kwargs,
    ):
        self.enabled = enabled
        self.host_name = host_name
        self.path = path
        self.tls = tls
        self.annotations = annotations
