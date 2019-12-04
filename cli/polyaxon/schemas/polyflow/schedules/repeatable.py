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
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


class RepeatableScheduleSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("repeatable"))
    limit = RefOrObject(
        fields.Int(required=True, validate=validate.Range(min=1)), required=True
    )
    depends_on_past = RefOrObject(fields.Bool(allow_none=True), required=True)

    @staticmethod
    def schema_config():
        return RepeatableScheduleConfig


class RepeatableScheduleConfig(BaseConfig):
    SCHEMA = RepeatableScheduleSchema
    IDENTIFIER = "repeatable"

    def __init__(self, limit=None, depends_on_past=None, kind=IDENTIFIER):
        self.limit = limit
        self.depends_on_past = depends_on_past
        self.kind = kind
