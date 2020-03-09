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

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon.polyflow.component.component import ComponentSchema
from polyaxon.polyflow.io.params import ParamSchema
from polyaxon.polyflow.operations.base import BaseOp, BaseOpSchema
from polyaxon.polyflow.references import (
    V1DagReference,
    V1HubReference,
    V1PathReference,
    V1UrlReference,
)
from polyaxon.polyflow.run import RunSchema


class OperationSchema(BaseOpSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("operation"))
    params = fields.Dict(
        keys=fields.Str(), values=fields.Nested(ParamSchema), allow_none=True
    )
    run_patch = fields.Nested(RunSchema, allow_none=True)
    hub_ref = fields.Str(allow_none=True)
    dag_ref = fields.Str(allow_none=True)
    url_ref = fields.Str(allow_none=True)
    path_ref = fields.Str(allow_none=True)
    component = fields.Nested(ComponentSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return V1Operation

    @validates_schema
    def validate_reference(self, data, **kwargs):
        count = 0
        hub_ref = data.get("hub_ref")
        if hub_ref:
            count += 1
        dag_ref = data.get("dag_ref")
        if dag_ref:
            count += 1
        url_ref = data.get("url_ref")
        if url_ref:
            count += 1
        path_ref = data.get("path_ref")
        if path_ref:
            count += 1
        component = data.get("component")
        if component and count == 0:
            count += 1

        if count != 1:
            raise ValidationError(
                "One and only one reference must be specified: "
                "hub_ref, dag_ref, url_ref, path_ref, component."
            )


class V1Operation(BaseOp, polyaxon_sdk.V1Operation):
    SCHEMA = OperationSchema
    IDENTIFIER = "operation"
    REDUCED_ATTRIBUTES = BaseOp.REDUCED_ATTRIBUTES + [
        "params",
        "hubRef",
        "dagRef",
        "urlRef",
        "pathRef",
        "component",
        "runPatch",
    ]

    @property
    def has_component_reference(self) -> bool:
        return self.component is not None

    @property
    def has_dag_reference(self) -> bool:
        return bool(self.dag_ref)

    @property
    def has_hub_reference(self) -> bool:
        return bool(self.hub_ref)

    @property
    def has_path_reference(self) -> bool:
        return bool(self.path_ref)

    @property
    def has_url_reference(self) -> bool:
        return bool(self.url_ref)

    @property
    def reference(self):
        if self.has_component_reference:
            return self.component
        if self.has_dag_reference:
            return V1DagReference(name=self.dag_ref)
        if self.has_hub_reference:
            return V1HubReference(name=self.hub_ref)
        if self.has_path_reference:
            return V1PathReference(path=self.path_ref)
        if self.has_url_reference:
            return V1UrlReference(url=self.url_ref)

    @property
    def template(self):
        if self.has_component_reference:
            return self.component
        if self.has_dag_reference:
            return V1DagReference(name=self.dag_ref)
        if self.has_hub_reference:
            return V1HubReference(name=self.hub_ref)
        if self.has_path_reference:
            return V1PathReference(path=self.path_ref)
        if self.has_url_reference:
            return V1UrlReference(url=self.url_ref)

    def set_template(self, value):
        self.component = value
