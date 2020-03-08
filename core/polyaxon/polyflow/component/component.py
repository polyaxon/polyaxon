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

import polyaxon_sdk

from marshmallow import fields, validate

from polyaxon.polyflow.component.base import BaseComponent, BaseComponentSchema
from polyaxon.polyflow.io import IOSchema
from polyaxon.polyflow.references import RefMixin
from polyaxon.polyflow.run import RunMixin, RunSchema
from polyaxon.schemas.base import NAME_REGEX


class ComponentSchema(BaseComponentSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("component"))
    tag = fields.Str(validate=validate.Regexp(regex=NAME_REGEX), allow_none=True)
    inputs = fields.Nested(IOSchema, allow_none=True, many=True)
    outputs = fields.Nested(IOSchema, allow_none=True, many=True)
    run = fields.Nested(RunSchema, required=True)

    @staticmethod
    def schema_config():
        return V1Component


class V1Component(BaseComponent, RunMixin, RefMixin, polyaxon_sdk.V1Component):
    SCHEMA = ComponentSchema
    IDENTIFIER = "component"
    REDUCED_ATTRIBUTES = BaseComponent.REDUCED_ATTRIBUTES + [
        "tag",
        "inputs",
        "outputs",
        "run",
    ]

    def get_run_kind(self):
        return self.run.kind if self.run else None

    def get_kind_value(self):
        return self.name

    def get_run_dict(self):
        config_dict = self.to_light_dict()
        config_dict.pop("tag", None)
        return config_dict
