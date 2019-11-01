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

from marshmallow import fields, validate

from polyaxon.schemas.base import BaseConfig, BaseOneOfSchema, BaseSchema
from polyaxon.schemas.polyflow.trigger_policies import (
    ExpressionTriggerPolicy,
    StatusTriggerPolicy,
)


class StatusConditionSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("status"))
    op = fields.Str()
    trigger = fields.Str(
        allow_none=True, validate=validate.OneOf(StatusTriggerPolicy.VALUES)
    )

    @staticmethod
    def schema_config():
        return StatusConditionConfig


class StatusConditionConfig(BaseConfig):
    SCHEMA = StatusConditionSchema
    IDENTIFIER = "status"

    def __init__(self, op, trigger, kind=None):
        self.op = op
        self.trigger = trigger
        self.kind = kind


class OutputsConditionSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("outputs"))
    op = fields.Str()
    exp = fields.Str(
        allow_none=True, validate=validate.OneOf(ExpressionTriggerPolicy.VALUES)
    )
    params = env_vars = fields.List(
        fields.List(fields.Raw(), validate=validate.Length(equal=2))
    )

    @staticmethod
    def schema_config():
        return OutputsConditionConfig


class OutputsConditionConfig(BaseConfig):
    SCHEMA = OutputsConditionSchema
    IDENTIFIER = "outputs"

    def __init__(self, op, exp, params, kind=None):
        self.op = op
        self.exp = exp
        self.params = params
        self.kind = kind


class ConditionSchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        StatusConditionConfig.IDENTIFIER: StatusConditionSchema,
        OutputsConditionConfig.IDENTIFIER: OutputsConditionSchema,
    }
