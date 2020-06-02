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


class AuthSchema(BaseCamelSchema):
    enabled = fields.Bool(allow_none=True)
    external = fields.Str(allow_none=True)
    use_resolver = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return AuthConfig


class AuthConfig(BaseConfig):
    SCHEMA = AuthSchema
    REDUCED_ATTRIBUTES = ["enabled", "external", "useResolver"]

    def __init__(self, enabled=None, external=None, use_resolver=None):
        self.enabled = enabled
        self.external = external
        self.use_resolver = use_resolver
