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
from polyaxon.schemas.polyflow.container import ContainerSchema
from polyaxon.schemas.polyflow.io import IOSchema


def validate_component(data):
    if not data.get("container") and not data.get("workflow"):
        raise ValidationError(
            "An component requires a container or a workflow section."
        )


class ComponentSchema(BaseComponentSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("component"))
    inputs = fields.Nested(IOSchema, allow_none=True, many=True)
    outputs = fields.Nested(IOSchema, allow_none=True, many=True)
    container = fields.Nested(ContainerSchema)

    @staticmethod
    def schema_config():
        return ComponentConfig

    @validates_schema
    def validate_component(self, data):
        validate_component(data)


class ComponentConfig(BaseComponentConfig):
    SCHEMA = ComponentSchema
    IDENTIFIER = "component"
    REDUCED_ATTRIBUTES = BaseComponentConfig.REDUCED_ATTRIBUTES + [
        "inputs",
        "outputs",
        "container",
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
        service=None,
        container=None,
        inputs=None,
        outputs=None,
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
            service=service,
        )
        validate_component({"container": container, "workflow": workflow})
        self.container = container
        self.inputs = inputs
        self.outputs = outputs
