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
from polyaxon_sdk import V1Hyperband, V1OptimizationResource

from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.polyflow.early_stopping import EarlyStoppingSchema
from polyaxon.schemas.polyflow.optimization import (
    OptimizationMetricSchema,
    ResourceType,
)
from polyaxon.schemas.polyflow.parallel.matrix import MatrixSchema


class ResourceSchema(BaseSchema):
    name = fields.Str()
    type = fields.Str(allow_none=True, validate=validate.OneOf(ResourceType.VALUES))

    @staticmethod
    def schema_config():
        return ResourceConfig


class ResourceConfig(BaseConfig, V1OptimizationResource):
    SCHEMA = ResourceSchema
    IDENTIFIER = "resource"

    def cast_value(self, value):
        if ResourceType.is_int(self.type):
            return int(value)
        if ResourceType.is_float(self.type):
            return float(value)
        return value


class HyperbandSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("hyperband"))
    matrix = fields.Dict(
        keys=fields.Str(), values=fields.Nested(MatrixSchema), allow_none=True
    )
    max_iter = RefOrObject(fields.Int(validate=validate.Range(min=1)))
    eta = RefOrObject(fields.Float(validate=validate.Range(min=0)))
    resource = fields.Nested(ResourceSchema)
    metric = fields.Nested(OptimizationMetricSchema)
    resume = RefOrObject(fields.Boolean(allow_none=True))
    seed = RefOrObject(fields.Int(allow_none=True))
    concurrency = fields.Int(allow_none=True)
    early_stopping = fields.Nested(EarlyStoppingSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return HyperbandConfig


class HyperbandConfig(BaseConfig, V1Hyperband):
    SCHEMA = HyperbandSchema
    IDENTIFIER = "hyperband"
    REDUCED_ATTRIBUTES = ["seed", "concurrency", "early_stopping"]
    IDENTIFIER_KIND = True
