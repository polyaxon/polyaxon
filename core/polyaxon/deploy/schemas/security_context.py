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

from marshmallow import ValidationError, fields, validates_schema

from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


def validate_security_context(user, group):
    if any([user, group]) and not all([user, group]):
        raise ValidationError(
            "Security context requires both `user` and `group` or none."
        )


class SecurityContextSchema(BaseCamelSchema):
    enabled = fields.Bool(allow_none=True)
    user = fields.Int(allow_none=True)
    group = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return SecurityContextConfig

    @validates_schema
    def validate_security_context(self, data, **kwargs):
        validate_security_context(data.get("user"), data.get("group"))


class SecurityContextConfig(BaseConfig):
    SCHEMA = SecurityContextSchema
    REDUCED_ATTRIBUTES = ["enabled", "user", "group"]

    def __init__(self, enabled=None, user=None, group=None):
        validate_security_context(user, group)
        self.enabled = enabled
        self.user = user
        self.group = group
