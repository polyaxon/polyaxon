# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load, validate, post_dump, validates_schema, \
    ValidationError

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.logging import LoggingSchema, LoggingConfig
from polyaxon_schemas.utils import Optimization, EarlyStopPolicy


class EarlyStoppingMetricSchema(Schema):
    metric = fields.Str()
    value = fields.Float()
    optimization = fields.Str(allow_none=True, validate=validate.OneOf(Optimization.VALUES))
    policy = fields.Str(allow_none=True, validate=validate.OneOf(EarlyStopPolicy.VALUES))

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return EarlyStoppingMetricConfig(**data)

    @post_dump
    def unmake(self, data):
        return EarlyStoppingMetricConfig.remove_reduced_attrs(data)


class EarlyStoppingMetricConfig(BaseConfig):
    SCHEMA = EarlyStoppingMetricSchema
    IDENTIFIER = 'early_stopping_metric'

    def __init__(self,
                 metric,
                 value=None,
                 optimization=Optimization.MAXIMIZE,
                 policy=EarlyStopPolicy.ALL):
        self.metric = metric
        self.value = value
        self.optimization = optimization
        self.policy = policy


class RandomSearchSchema(Schema):
    n_experiments = fields.Int(allow_none=True, validate=validate.Range(min=0))

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return RandomSearchConfig(**data)

    @post_dump
    def unmake(self, data):
        return RandomSearchConfig.remove_reduced_attrs(data)


class RandomSearchConfig(BaseConfig):
    SCHEMA = RandomSearchSchema
    IDENTIFIER = 'random_search'

    def __init__(self, n_experiments):
        self.n_experiments = n_experiments


class HyperBandSchema(Schema):
    max_iter = fields.Int(allow_none=True, validate=validate.Range(min=0))
    eta = fields.Int(allow_none=True, validate=validate.Range(min=0))

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return HyperBandConfig(**data)

    @post_dump
    def unmake(self, data):
        return HyperBandConfig.remove_reduced_attrs(data)


class HyperBandConfig(BaseConfig):
    SCHEMA = HyperBandSchema
    IDENTIFIER = 'hyperband'

    def __init__(self, max_iter, eta=3):
        self.max_iter = max_iter
        self.eta = eta


def validate_search_algorithm(frameworks):
    if sum([1 for f in frameworks if f is not None]) > 1:
        raise ValidationError('Only one search algorithm can be used.')


class SettingsSchema(Schema):
    logging = fields.Nested(LoggingSchema, allow_none=True)
    seed = fields.Int(allow_none=True)
    matrix = fields.Dict(allow_none=True)
    concurrent_experiments = fields.Int(allow_none=True)
    random_search = fields.Nested(RandomSearchSchema, allow_none=None)
    hyperband = fields.Nested(HyperBandSchema, allow_none=None)
    early_stopping = fields.Nested(EarlyStoppingMetricSchema, many=True, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return SettingsConfig(**data)

    @post_dump
    def unmake(self, data):
        return SettingsConfig.remove_reduced_attrs(data)

    @validates_schema
    def validate_quantity(self, data):
        validate_search_algorithm([data.get('random_search'),
                                   data.get('hyperband'),
                                   data.get('pytorch'),
                                   data.get('horovod')])


class SettingsConfig(BaseConfig):
    SCHEMA = SettingsSchema
    IDENTIFIER = 'settings'

    def __init__(self,
                 logging=LoggingConfig(),
                 seed=None,
                 matrix=None,
                 concurrent_experiments=1,
                 random_search=None,
                 hyperband=None,
                 n_experiments=None,
                 early_stopping=None):
        self.logging = logging
        self.seed = seed
        self.matrix = matrix
        self.concurrent_experiments = concurrent_experiments
        validate_search_algorithm([random_search, hyperband])
        self.random_search = random_search
        self.hyperband = hyperband
        self.n_experiments = (int(n_experiments)
                              if (n_experiments and n_experiments >= 1)
                              else n_experiments)
        self.early_stopping = early_stopping
