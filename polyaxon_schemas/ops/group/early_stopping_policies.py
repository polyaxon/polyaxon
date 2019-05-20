# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.base import BaseConfig, BaseOneOfSchema, BaseSchema
from polyaxon_schemas.ops.group.metrics import Optimization


class MedianStoppingPolicySchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal('median'))
    evaluation_interval = fields.Int()

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

    IDENTIFIER = 'median'
    SCHEMA = MedianStoppingPolicySchema

    def __init__(self,
                 evaluation_interval,
                 kind='median'):
        self.kind = kind
        self.evaluation_interval = evaluation_interval


class AverageStoppingPolicySchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal('average'))
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

    IDENTIFIER = 'average'
    SCHEMA = AverageStoppingPolicySchema

    def __init__(self,
                 evaluation_interval,
                 kind='average'):
        self.kind = kind
        self.evaluation_interval = evaluation_interval


class TruncationStoppingPolicySchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal('truncation'))
    percent = fields.Int()
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

    IDENTIFIER = 'truncation'
    SCHEMA = TruncationStoppingPolicySchema

    def __init__(self,
                 percent,
                 evaluation_interval,
                 kind='truncation'):
        self.kind = kind
        self.percent = percent
        self.evaluation_interval = evaluation_interval


class StoppingPolicySchema(BaseOneOfSchema):
    TYPE_FIELD = 'kind'
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        MedianStoppingPolicyConfig.IDENTIFIER: MedianStoppingPolicySchema,
        AverageStoppingPolicyConfig.IDENTIFIER: AverageStoppingPolicySchema,
        TruncationStoppingPolicyConfig.IDENTIFIER: TruncationStoppingPolicySchema,
    }


class EarlyStoppingSchema(BaseSchema):
    metric = fields.Str()
    value = fields.Float()
    optimization = fields.Str(allow_none=True, validate=validate.OneOf(Optimization.VALUES))
    policy = fields.Nested(StoppingPolicySchema, allow_none=True)

    @staticmethod
    def schema_config():
        return EarlyStoppingConfig


class EarlyStoppingConfig(BaseConfig):
    """
    Early stopping metric config.

    Args:
        metric: `str`. The metric to use for early stopping.
        value: `float`. The metric value to use for the condition.
        optimization: `string`. The optimization to do: maximize or minimize.
        policy: `Dict`. Optional, the termination policy to use.
    """
    SCHEMA = EarlyStoppingSchema
    IDENTIFIER = 'early_stopping_metric'

    def __init__(self,
                 metric,
                 value=None,
                 optimization=Optimization.MAXIMIZE,
                 policy=None):
        self.metric = metric
        self.value = value
        self.optimization = optimization
        self.policy = policy
