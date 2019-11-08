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

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon.schemas.polyflow.base import BaseComponentConfig, BaseComponentSchema
from polyaxon.schemas.polyflow.component import ComponentSchema
from polyaxon.schemas.polyflow.component_ref import ComponentRefSchema
from polyaxon.schemas.polyflow.conditions import ConditionSchema
from polyaxon.schemas.polyflow.trigger_policies import TriggerPolicy


def validate_op(data):
    if not data.get("component") and not data.get("component_ref"):
        raise ValidationError("An op requires an component or a component_ref section.")


class OpSchema(BaseComponentSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("op"))
    dependencies = fields.List(fields.Str(), allow_none=True)
    trigger = fields.Str(allow_none=True, validate=validate.OneOf(TriggerPolicy.VALUES))
    conditions = fields.Nested(ConditionSchema, allow_none=True)
    skip_on_upstream_skip = fields.Bool(allow_none=True)
    params = fields.Raw(allow_none=True)
    component_ref = fields.Nested(ComponentRefSchema, allow_none=True)
    component = fields.Nested(ComponentSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return OpConfig

    @validates_schema
    def validate_op(self, data):
        validate_op(data)


class OpConfig(BaseComponentConfig):
    SCHEMA = OpSchema
    IDENTIFIER = "op"
    REDUCED_ATTRIBUTES = BaseComponentConfig.REDUCED_ATTRIBUTES + [
        "params",
        "dependencies",
        "trigger",
        "conditions",
        "skip_on_upstream_skip",
        "component_ref",
        "component",
    ]

    def __init__(
        self,
        version=None,
        kind=None,
        name=None,
        description=None,
        tags=None,
        profile=None,
        nocache=None,
        environment=None,
        termination=None,
        init=None,
        mounts=None,
        schedule=None,
        workflow=None,
        recursive=None,
        service=None,
        dependencies=None,
        params=None,
        trigger=None,
        conditions=None,
        skip_on_upstream_skip=None,
        component_ref=None,
        component=None,
    ):
        super().__init__(
            version=version,
            kind=kind,
            name=name,
            description=description,
            tags=tags,
            profile=profile,
            nocache=nocache,
            environment=environment,
            termination=termination,
            init=init,
            mounts=mounts,
            schedule=schedule,
            workflow=workflow,
            recursive=recursive,
            service=service,
        )
        validate_op({"component_ref": component_ref, "component": component})
        self.component_ref = component_ref
        self.params = params
        self.dependencies = dependencies
        self.trigger = trigger
        self.conditions = conditions
        self.skip_on_upstream_skip = skip_on_upstream_skip
        self.component = component
