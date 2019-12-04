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
from polyaxon_sdk import V1Component

from polyaxon.schemas.polyflow.base import BaseComponentConfig, BaseComponentSchema
from polyaxon.schemas.polyflow.io import IOSchema
from polyaxon.schemas.polyflow.run import RunMixin, RunSchema


class ComponentSchema(BaseComponentSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("component"))
    inputs = fields.Nested(IOSchema, allow_none=True, many=True)
    outputs = fields.Nested(IOSchema, allow_none=True, many=True)
    run = fields.Nested(RunSchema, required=True)

    @staticmethod
    def schema_config():
        return ComponentConfig


class ComponentConfig(BaseComponentConfig, RunMixin, V1Component):
    SCHEMA = ComponentSchema
    IDENTIFIER = "component"
    REDUCED_ATTRIBUTES = BaseComponentConfig.REDUCED_ATTRIBUTES + [
        "inputs",
        "outputs",
        "run",
    ]
    IDENTIFIER_KIND = True

    def get_run_kind(self):
        return self.run.kind if self.run else None
