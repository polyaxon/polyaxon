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

from marshmallow import ValidationError, fields, validates_schema

from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.utils.signal_decorators import check_partial


def validate_security_context(user, group):
    if any([user, group]) and not all([user, group]):
        raise ValidationError(
            "Security context requires both `user` and `group` or none."
        )


class SecurityContextSchema(BaseCamelSchema):
    enabled = fields.Bool(allow_none=True)
    run_as_user = fields.Int(allow_none=True)
    run_as_group = fields.Int(allow_none=True)
    fs_group = fields.Int(allow_none=True)
    fs_group_change_policy = fields.Str(allow_none=True)
    allow_privilege_escalation = fields.Bool(allow_none=True)
    run_as_non_root = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return SecurityContextConfig

    @validates_schema
    @check_partial
    def validate_security_context(self, data, **kwargs):
        validate_security_context(data.get("run_as_user"), data.get("run_as_group"))


class SecurityContextConfig(BaseConfig):
    SCHEMA = SecurityContextSchema
    REDUCED_ATTRIBUTES = [
        "enabled",
        "runAsUser",
        "runAsGroup",
        "fsGroup",
        "fsGroupChangePolicy",
        "allowPrivilegeEscalation",
        "runAsNonRoot",
    ]

    def __init__(
        self,
        enabled=None,
        run_as_user=None,
        run_as_group=None,
        fs_group=None,
        fs_group_change_policy=None,
        allow_privilege_escalation=None,
        run_as_non_root=None,
    ):
        validate_security_context(run_as_user, run_as_group)
        self.enabled = enabled
        self.run_as_user = run_as_user
        self.run_as_group = run_as_group
        self.fs_group = fs_group
        self.fs_group_change_policy = fs_group_change_policy
        self.allow_privilege_escalation = allow_privilege_escalation
        self.run_as_non_root = run_as_non_root
