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

from polyaxon.polyflow.optimization import Optimization
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig, BaseOneOfSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject


class MedianStoppingPolicySchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("median"))
    evaluation_interval = RefOrObject(fields.Int(), required=True)
    min_interval = RefOrObject(fields.Int(allow_none=True))
    min_samples = RefOrObject(fields.Int(allow_none=True))

    @staticmethod
    def schema_config():
        return V1MedianStoppingPolicy


class V1MedianStoppingPolicy(BaseConfig, polyaxon_sdk.V1MedianStoppingPolicy):
    IDENTIFIER = "median"
    SCHEMA = MedianStoppingPolicySchema
    REDUCED_ATTRIBUTES = ["minInterval", "minSamples"]


class TruncationStoppingPolicySchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("truncation"))
    percent = RefOrObject(fields.Float(), required=True)
    evaluation_interval = RefOrObject(fields.Int(), required=True)
    min_interval = RefOrObject(fields.Int(allow_none=True))
    min_samples = RefOrObject(fields.Int(allow_none=True))

    @staticmethod
    def schema_config():
        return V1TruncationStoppingPolicy


class V1TruncationStoppingPolicy(BaseConfig, polyaxon_sdk.V1TruncationStoppingPolicy):
    IDENTIFIER = "truncation"
    SCHEMA = TruncationStoppingPolicySchema
    REDUCED_ATTRIBUTES = ["minInterval", "minSamples"]


class DiffStoppingPolicySchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("diff"))
    percent = RefOrObject(fields.Float(), required=True)
    evaluation_interval = RefOrObject(fields.Int(), required=True)
    min_interval = RefOrObject(fields.Int(allow_none=True))
    min_samples = RefOrObject(fields.Int(allow_none=True))

    @staticmethod
    def schema_config():
        return V1DiffStoppingPolicy


class V1DiffStoppingPolicy(BaseConfig, polyaxon_sdk.V1DiffStoppingPolicy):
    IDENTIFIER = "diff"
    SCHEMA = DiffStoppingPolicySchema
    REDUCED_ATTRIBUTES = ["minInterval", "minSamples"]


class StoppingPolicySchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        V1MedianStoppingPolicy.IDENTIFIER: MedianStoppingPolicySchema,
        V1TruncationStoppingPolicy.IDENTIFIER: TruncationStoppingPolicySchema,
        V1DiffStoppingPolicy.IDENTIFIER: DiffStoppingPolicySchema,
    }


class MetricEarlyStoppingSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("metric_early_stopping"))
    metric = RefOrObject(fields.Str(), required=True)
    value = RefOrObject(fields.Float(), required=True)
    optimization = RefOrObject(
        fields.Str(validate=validate.OneOf(Optimization.VALUES)), required=True
    )
    policy = fields.Nested(StoppingPolicySchema, allow_none=True)

    @staticmethod
    def schema_config():
        return V1MetricEarlyStopping


class V1MetricEarlyStopping(BaseConfig, polyaxon_sdk.V1MetricEarlyStopping):
    SCHEMA = MetricEarlyStoppingSchema
    IDENTIFIER = "metric_early_stopping"


class FailureEarlyStoppingSchema(BaseCamelSchema):
    kind = fields.Str(
        allow_none=True, validate=validate.Equal("failure_early_stopping")
    )
    percent = RefOrObject(fields.Float(), required=True)
    evaluation_interval = RefOrObject(fields.Int(), required=True)

    @staticmethod
    def schema_config():
        return V1FailureEarlyStopping


class V1FailureEarlyStopping(BaseConfig, polyaxon_sdk.V1FailureEarlyStopping):
    IDENTIFIER = "failure_early_stopping"
    SCHEMA = FailureEarlyStoppingSchema
