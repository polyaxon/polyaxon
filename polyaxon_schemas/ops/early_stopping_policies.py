# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.ops.metrics import Optimization


class MedianStoppingPolicySchema(BaseSchema):
    kind = fields.Str(allow_none=None, validate=validate.Equal('median'))
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
    kind = fields.Str(allow_none=None, validate=validate.Equal('average'))
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
    kind = fields.Str(allow_none=None, validate=validate.Equal('truncation'))
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


def validate_policy(policy):
    if not policy:
        return None

    if 'kind' not in policy:
        raise ValidationError('Policy kind is a required field.')

    if policy['kind'] == MedianStoppingPolicyConfig.IDENTIFIER:
        return MedianStoppingPolicyConfig.from_dict(policy)
    if policy['kind'] == AverageStoppingPolicyConfig.IDENTIFIER:
        return AverageStoppingPolicyConfig.from_dict(policy)
    if policy['kind'] == TruncationStoppingPolicyConfig.IDENTIFIER:
        return TruncationStoppingPolicyConfig.from_dict(policy)


class EarlyStoppingMetricSchema(BaseSchema):
    metric = fields.Str()
    value = fields.Float()
    optimization = fields.Str(allow_none=True, validate=validate.OneOf(Optimization.VALUES))
    policy = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return EarlyStoppingMetricConfig

    @validates_schema
    def validate_policy(self, data):
        """Validates policy data"""
        validate_policy(data.get('policy'))


class EarlyStoppingMetricConfig(BaseConfig):
    """
    Early stopping metric config.

    Args:
        metric: `str`. The metric to use for early stopping.
        value: `float`. The metric value to use for the condition.
        optimization: `string`. The optimization to do: maximize or minimize.
        policy: `Dict`. Optional, the termination policy to use.
    """
    SCHEMA = EarlyStoppingMetricSchema
    IDENTIFIER = 'early_stopping_metric'

    def __init__(self,
                 metric,
                 value=None,
                 optimization=Optimization.MAXIMIZE,
                 policy=None):
        self.policy_config = validate_policy(policy)
        self.metric = metric
        self.value = value
        self.optimization = optimization
        self.policy = policy
