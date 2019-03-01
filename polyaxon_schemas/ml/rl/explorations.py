# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema, BaseSchema


class BaseExplorationSchema(BaseSchema):
    is_continuous = fields.Bool(default=False, missing=False)

    @staticmethod
    def schema_config():
        return BaseExplorationConfig


class BaseExplorationConfig(BaseConfig):
    def __init__(self, is_continuous=False):
        self.is_continuous = is_continuous


class ConstantExplorationSchema(BaseExplorationSchema):
    value = fields.Float(default=0.5, missing=0.5)

    @staticmethod
    def schema_config():
        return ConstantExplorationConfig


class ConstantExplorationConfig(BaseExplorationConfig):
    IDENTIFIER = 'Constant'
    SCHEMA = ConstantExplorationSchema

    def __init__(self, value=0.5, is_continuous=False):
        self.value = value
        super(ConstantExplorationConfig, self).__init__(is_continuous)


class GreedyExplorationSchema(BaseExplorationSchema):

    @staticmethod
    def schema_config():
        return GreedyExplorationConfig


class GreedyExplorationConfig(BaseExplorationConfig):
    IDENTIFIER = 'Greedy'
    SCHEMA = GreedyExplorationSchema


class RandomExplorationSchema(BaseExplorationSchema):

    @staticmethod
    def schema_config():
        return RandomExplorationConfig


class RandomExplorationConfig(BaseExplorationConfig):
    IDENTIFIER = 'Random'
    SCHEMA = RandomExplorationSchema


class DecayExplorationSchema(BaseExplorationSchema):
    exploration_rate = fields.Float(allow_none=True)
    decay_type = fields.Str(allow_none=True, validate=validate.OneOf(
        ['exponential_decay', 'inverse_time_decay', 'natural_exp_decay', 'piecewise_constant',
         'polynomial_decay']))
    start_decay_at = fields.Int(allow_none=True)
    stop_decay_at = fields.Int(allow_none=True)
    decay_rate = fields.Float(allow_none=True)
    staircase = fields.Bool(allow_none=True)
    decay_steps = fields.Int(allow_none=True)
    min_exploration_rate = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return DecayExplorationConfig


class DecayExplorationConfig(BaseExplorationConfig):
    IDENTIFIER = 'Decay'
    SCHEMA = DecayExplorationSchema

    def __init__(self,
                 is_continuous=False,
                 exploration_rate=0.15,
                 decay_type='polynomial_decay',
                 start_decay_at=0,
                 stop_decay_at=1e9,
                 decay_rate=0.,
                 staircase=False,
                 decay_steps=100000,
                 min_exploration_rate=0):
        self.exploration_rate = exploration_rate
        self.decay_type = decay_type
        self.start_decay_at = start_decay_at
        self.stop_decay_at = stop_decay_at
        self.decay_rate = decay_rate
        self.staircase = staircase
        self.decay_steps = decay_steps
        self.min_exploration_rate = min_exploration_rate
        super(DecayExplorationConfig, self).__init__(is_continuous)


class RandomDecayExplorationSchema(BaseExplorationSchema):
    num_actions = fields.Int(allow_none=True)
    decay_type = fields.Str(allow_none=True, validate=validate.OneOf(
        ['exponential_decay', 'inverse_time_decay', 'natural_exp_decay', 'piecewise_constant',
         'polynomial_decay']))
    start_decay_at = fields.Int(allow_none=True)
    stop_decay_at = fields.Int(allow_none=True)
    decay_rate = fields.Float(allow_none=True)
    staircase = fields.Bool(allow_none=True)
    decay_steps = fields.Int(allow_none=True)
    min_exploration_rate = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return RandomDecayExplorationConfig


class RandomDecayExplorationConfig(BaseExplorationConfig):
    IDENTIFIER = 'RandomDecay'
    SCHEMA = RandomDecayExplorationSchema

    def __init__(self,
                 is_continuous=False,
                 num_actions=None,
                 decay_type='polynomial_decay',
                 start_decay_at=0,
                 stop_decay_at=1e9,
                 decay_rate=0.,
                 staircase=False,
                 decay_steps=10000,
                 min_exploration_rate=0):
        self.num_actions = num_actions
        self.decay_type = decay_type
        self.start_decay_at = start_decay_at
        self.stop_decay_at = stop_decay_at
        self.decay_rate = decay_rate
        self.staircase = staircase
        self.decay_steps = decay_steps
        self.min_exploration_rate = min_exploration_rate
        super(RandomDecayExplorationConfig, self).__init__(is_continuous)


class OrnsteinUhlenbeckExplorationSchema(BaseExplorationSchema):
    num_actions = fields.Int(allow_none=True)
    sigma = fields.Float(allow_none=True)
    mu = fields.Float(allow_none=True)
    theta = fields.Float(allow_none=True)

    @staticmethod
    def schema_config():
        return OrnsteinUhlenbeckExplorationConfig


class OrnsteinUhlenbeckExplorationConfig(BaseExplorationConfig):
    IDENTIFIER = 'OrnsteinUhlenbeck'
    SCHEMA = OrnsteinUhlenbeckExplorationSchema

    def __init__(self, num_actions, sigma=0.3, mu=0, theta=0.15, **kwargs):
        self.num_actions = num_actions
        self.sigma = sigma
        self.mu = mu
        self.theta = theta
        super(OrnsteinUhlenbeckExplorationConfig, self).__init__(True)


class RegularizerSchema(BaseMultiSchema):
    __multi_schema_name__ = 'exploration'
    __configs__ = {
        ConstantExplorationConfig.IDENTIFIER: ConstantExplorationConfig,
        GreedyExplorationConfig.IDENTIFIER: GreedyExplorationConfig,
        RandomExplorationConfig.IDENTIFIER: RandomExplorationConfig,
        DecayExplorationConfig.IDENTIFIER: DecayExplorationConfig,
        RandomDecayExplorationConfig.IDENTIFIER: RandomDecayExplorationConfig,
        OrnsteinUhlenbeckExplorationConfig.IDENTIFIER: OrnsteinUhlenbeckExplorationConfig
    }
