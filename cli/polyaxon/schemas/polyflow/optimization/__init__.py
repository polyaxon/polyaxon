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
from polyaxon_sdk import V1Optimization, V1OptimizationMetric, V1ResourceType


class ResourceType(V1ResourceType):
    INT = V1ResourceType.INT
    FLOAT = V1ResourceType.FLOAT

    INT_VALUES = {INT, INT.upper(), INT.capitalize()}
    FLOAT_VALUES = {FLOAT, FLOAT.upper(), FLOAT.capitalize()}

    VALUES = INT_VALUES | FLOAT_VALUES

    @classmethod
    def is_int(cls, value):
        return value in cls.INT_VALUES

    @classmethod
    def is_float(cls, value):
        return value in cls.FLOAT_VALUES


class Optimization(V1Optimization):
    MAXIMIZE = V1Optimization.MAXIMIZE
    MINIMIZE = V1Optimization.MINIMIZE

    MAXIMIZE_VALUES = [MAXIMIZE, MAXIMIZE.upper(), MAXIMIZE.capitalize()]
    MINIMIZE_VALUES = [MINIMIZE, MINIMIZE.upper(), MINIMIZE.capitalize()]

    VALUES = MAXIMIZE_VALUES + MINIMIZE_VALUES

    @classmethod
    def maximize(cls, value):
        return value in cls.MAXIMIZE_VALUES

    @classmethod
    def minimize(cls, value):
        return value in cls.MINIMIZE_VALUES


class OptimizationMetricSchema(BaseSchema):
    name = fields.Str()
    optimization = fields.Str(
        allow_none=True, validate=validate.OneOf(Optimization.VALUES)
    )

    @staticmethod
    def schema_config():
        return OptimizationMetricConfig


class OptimizationMetricConfig(BaseConfig, V1OptimizationMetric):
    SCHEMA = OptimizationMetricSchema
    IDENTIFIER = "search_metric"
    IDENTIFIER_KIND = True
