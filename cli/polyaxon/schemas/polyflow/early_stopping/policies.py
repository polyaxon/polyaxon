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
from polyaxon_sdk import (
    V1AverageStoppingPolicy,
    V1FailureEarlyStopping,
    V1MedianStoppingPolicy,
    V1MetricEarlyStopping,
    V1TruncationStoppingPolicy,
)

from polyaxon.schemas.base import BaseConfig, BaseOneOfSchema, BaseSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.polyflow.optimization import Optimization


class MedianStoppingPolicySchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("median"))
    evaluation_interval = fields.Int(required=True)

    @staticmethod
    def schema_config():
        return MedianStoppingPolicyConfig


class MedianStoppingPolicyConfig(BaseConfig, V1MedianStoppingPolicy):
    IDENTIFIER = "median"
    SCHEMA = MedianStoppingPolicySchema
    IDENTIFIER_KIND = True


class AverageStoppingPolicySchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("average"))
    evaluation_interval = fields.Int()

    @staticmethod
    def schema_config():
        return AverageStoppingPolicyConfig


class AverageStoppingPolicyConfig(BaseConfig, V1AverageStoppingPolicy):
    IDENTIFIER = "average"
    SCHEMA = AverageStoppingPolicySchema
    IDENTIFIER_KIND = True


class TruncationStoppingPolicySchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("truncation"))
    percent = fields.Float()
    evaluation_interval = fields.Int()

    @staticmethod
    def schema_config():
        return TruncationStoppingPolicyConfig


class TruncationStoppingPolicyConfig(BaseConfig, V1TruncationStoppingPolicy):
    IDENTIFIER = "truncation"
    SCHEMA = TruncationStoppingPolicySchema
    IDENTIFIER_KIND = True


class StoppingPolicySchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        MedianStoppingPolicyConfig.IDENTIFIER: MedianStoppingPolicySchema,
        AverageStoppingPolicyConfig.IDENTIFIER: AverageStoppingPolicySchema,
        TruncationStoppingPolicyConfig.IDENTIFIER: TruncationStoppingPolicySchema,
    }


class MetricEarlyStoppingSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("metric_early_stopping"))
    metric = fields.Str()
    value = RefOrObject(fields.Float())
    optimization = fields.Str(
        allow_none=True, validate=validate.OneOf(Optimization.VALUES)
    )
    policy = fields.Nested(StoppingPolicySchema, allow_none=True)

    @staticmethod
    def schema_config():
        return MetricEarlyStoppingConfig


class MetricEarlyStoppingConfig(BaseConfig, V1MetricEarlyStopping):
    SCHEMA = MetricEarlyStoppingSchema
    IDENTIFIER = "metric_early_stopping"
    IDENTIFIER_KIND = True


class FailureEarlyStoppingSchema(BaseSchema):
    kind = fields.Str(
        allow_none=True, validate=validate.Equal("failure_early_stopping")
    )
    percent = fields.Float()
    evaluation_interval = RefOrObject(fields.Int())

    @staticmethod
    def schema_config():
        return FailureEarlyStoppingConfig


class FailureEarlyStoppingConfig(BaseConfig, V1FailureEarlyStopping):
    IDENTIFIER = "failure_early_stopping"
    SCHEMA = FailureEarlyStoppingSchema
    IDENTIFIER_KIND = True
