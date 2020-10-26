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

from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class ResourceType(polyaxon_sdk.V1ResourceType):
    INT = polyaxon_sdk.V1ResourceType.INT
    FLOAT = polyaxon_sdk.V1ResourceType.FLOAT

    INT_VALUES = {INT, INT.upper(), INT.capitalize()}
    FLOAT_VALUES = {FLOAT, FLOAT.upper(), FLOAT.capitalize()}

    VALUES = INT_VALUES | FLOAT_VALUES

    @classmethod
    def is_int(cls, value):
        return value in cls.INT_VALUES

    @classmethod
    def is_float(cls, value):
        return value in cls.FLOAT_VALUES


class V1Optimization(polyaxon_sdk.V1Optimization):
    MAXIMIZE = polyaxon_sdk.V1Optimization.MAXIMIZE
    MINIMIZE = polyaxon_sdk.V1Optimization.MINIMIZE

    MAXIMIZE_VALUES = [MAXIMIZE, MAXIMIZE.upper(), MAXIMIZE.capitalize()]
    MINIMIZE_VALUES = [MINIMIZE, MINIMIZE.upper(), MINIMIZE.capitalize()]

    VALUES = MAXIMIZE_VALUES + MINIMIZE_VALUES

    @classmethod
    def maximize(cls, value):
        return value in cls.MAXIMIZE_VALUES

    @classmethod
    def minimize(cls, value):
        return value in cls.MINIMIZE_VALUES


class OptimizationMetricSchema(BaseCamelSchema):
    name = fields.Str()
    optimization = fields.Str(
        allow_none=True, validate=validate.OneOf(V1Optimization.VALUES)
    )

    @staticmethod
    def schema_config():
        return V1OptimizationMetric


class V1OptimizationMetric(BaseConfig, polyaxon_sdk.V1OptimizationMetric):
    SCHEMA = OptimizationMetricSchema
    IDENTIFIER = "optimization_metric"

    def get_for_sort(self):
        if self.optimization == V1Optimization.MINIMIZE:
            return self.name
        return "-{}".format(self.name)


class OptimizationResourceSchema(BaseCamelSchema):
    name = fields.Str()
    type = fields.Str(allow_none=True, validate=validate.OneOf(ResourceType.VALUES))

    @staticmethod
    def schema_config():
        return V1OptimizationResource


class V1OptimizationResource(BaseConfig, polyaxon_sdk.V1OptimizationResource):
    SCHEMA = OptimizationResourceSchema
    IDENTIFIER = "optimization_resource"

    def cast_value(self, value):
        if ResourceType.is_int(self.type):
            return int(value)
        if ResourceType.is_float(self.type):
            return float(value)
        return value
