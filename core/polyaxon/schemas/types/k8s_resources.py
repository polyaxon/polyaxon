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

from marshmallow import fields

from polyaxon.connections.schemas import K8sResourceSchema
from polyaxon.schemas.base import BaseCamelSchema
from polyaxon.schemas.types.base import BaseTypeConfig


class K8sResourceTypeSchema(BaseCamelSchema):
    name = fields.Str(required=True)
    schema = fields.Nested(K8sResourceSchema, allow_none=True)
    is_requested = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return V1K8sResourceType


class V1K8sResourceType(BaseTypeConfig, polyaxon_sdk.V1K8sResourceType):
    IDENTIFIER = "secret_resource"
    SCHEMA = K8sResourceTypeSchema
    REDUCED_ATTRIBUTES = ["name", "schema", "isRequested"]

    @classmethod
    def from_model(cls, model, is_requested=False) -> "V1K8sResourceType":
        schema = model.schema
        if hasattr(schema, "to_dict"):
            schema = schema.to_dict()
        return V1K8sResourceType.from_dict(
            {"name": model.name, "schema": schema, "isRequested": is_requested}
        )
