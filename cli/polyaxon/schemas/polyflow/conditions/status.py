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

from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.polyflow.trigger_policies import StatusTriggerPolicy


class StatusConditionSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("status"))
    op = fields.Str(required=True)
    trigger = fields.Str(
        required=True, validate=validate.OneOf(StatusTriggerPolicy.VALUES)
    )

    @staticmethod
    def schema_config():
        return StatusConditionConfig


class StatusConditionConfig(BaseConfig):
    SCHEMA = StatusConditionSchema
    IDENTIFIER = "status"

    def __init__(self, op=None, trigger=None, kind=None):
        self.op = op
        self.trigger = trigger
        self.kind = kind
