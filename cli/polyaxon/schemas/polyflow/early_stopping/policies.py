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

from polyaxon.schemas.base import BaseConfig, BaseOneOfSchema, BaseSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.polyflow.optimization import Optimization


class MedianStoppingPolicySchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("median"))
    evaluation_interval = fields.Int(required=True)

    @staticmethod
    def schema_config():
        return MedianStoppingPolicyConfig


class MedianStoppingPolicyConfig(BaseConfig):
    """
    Early stopping with median stopping, this policy computes running medians across
    all experiments and stops those whose best performance is worse than the median
    of the running experiments.

    Args:
        evaluation_interval: `int`. Frequency for applying the policy.
    """

    IDENTIFIER = "median"
    SCHEMA = MedianStoppingPolicySchema

    def __init__(self, evaluation_interval, kind=IDENTIFIER):
        self.kind = kind
        self.evaluation_interval = evaluation_interval


class AverageStoppingPolicySchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("average"))
    evaluation_interval = fields.Int()

    @staticmethod
    def schema_config():
        return AverageStoppingPolicyConfig


class AverageStoppingPolicyConfig(BaseConfig):
    """
    Early stopping with average stopping, this policy computes running averages across
    all experiments and stops those whose best performance is worse than the median
    of the running experiments.

    Args:
        evaluation_interval: `int`. Frequency for applying the policy.
    """

    IDENTIFIER = "average"
    SCHEMA = AverageStoppingPolicySchema

    def __init__(self, evaluation_interval, kind=IDENTIFIER):
        self.kind = kind
        self.evaluation_interval = evaluation_interval


class TruncationStoppingPolicySchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("truncation"))
    percent = fields.Float()
    evaluation_interval = fields.Int()

    @staticmethod
    def schema_config():
        return TruncationStoppingPolicyConfig


class TruncationStoppingPolicyConfig(BaseConfig):
    """
    Early stopping with truncation stopping, this policy stops a percentage of
    all running experiments at every evaluation.

    Args:
        percent: `int`. e.g. 1 - 99. The percentage of experiments to stop,
                 at each evaluation interval.
        evaluation_interval: `int`. Frequency for applying the policy.
    """

    IDENTIFIER = "truncation"
    SCHEMA = TruncationStoppingPolicySchema

    def __init__(self, percent, evaluation_interval, kind=IDENTIFIER):
        self.kind = kind
        self.percent = percent
        self.evaluation_interval = evaluation_interval


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


class MetricEarlyStoppingConfig(BaseConfig):
    """
    Early stopping based on metric config.

    Args:
        metric: `str`. The metric to use for early stopping.
        value: `float`. The metric value to use for the condition.
        optimization: `string`. The optimization to do: maximize or minimize.
        policy: `Dict`. Optional, the termination policy to use.
    """

    SCHEMA = MetricEarlyStoppingSchema
    IDENTIFIER = "metric_early_stopping"

    def __init__(
        self,
        metric,
        value=None,
        optimization=Optimization.MAXIMIZE,
        policy=None,
        kind=IDENTIFIER,
    ):
        self.kind = kind
        self.metric = metric
        self.value = value
        self.optimization = optimization
        self.policy = policy


class FailureEarlyStoppingSchema(BaseSchema):
    kind = fields.Str(
        allow_none=True, validate=validate.Equal("failure_early_stopping")
    )
    percent = fields.Float()
    evaluation_interval = RefOrObject(fields.Int())

    @staticmethod
    def schema_config():
        return FailureEarlyStoppingConfig


class FailureEarlyStoppingConfig(BaseConfig):
    """
    Early stopping with failure rate stopping, this policy stops based on a percentage of
    failed experiments at every evaluation.

    Args:
        percent: `int`. e.g. 1 - 99. The percentage of experiments to stop,
                 at each evaluation interval.
        evaluation_interval: `int`. Frequency for applying the policy.
    """

    IDENTIFIER = "failure_early_stopping"
    SCHEMA = FailureEarlyStoppingSchema

    def __init__(self, percent, evaluation_interval=None, kind=IDENTIFIER):
        self.kind = kind
        self.percent = percent
        self.evaluation_interval = evaluation_interval
