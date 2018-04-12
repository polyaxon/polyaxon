# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from marshmallow import (
    Schema,
    ValidationError,
    fields,
    post_dump,
    post_load,
    validate,
    validates_schema
)

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.logging import LoggingConfig, LoggingSchema
from polyaxon_schemas.matrix import MatrixConfig
from polyaxon_schemas.utils import EarlyStoppingPolicy, Optimization


class EarlyStoppingMetricSchema(Schema):
    metric = fields.Str()
    value = fields.Float()
    optimization = fields.Str(allow_none=True, validate=validate.OneOf(Optimization.VALUES))
    policy = fields.Str(allow_none=True, validate=validate.OneOf(EarlyStoppingPolicy.VALUES))

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
                 policy=EarlyStoppingPolicy.ALL):
        self.metric = metric
        self.value = value
        self.optimization = optimization
        self.policy = policy


class RandomSearchSchema(Schema):
    n_experiments = fields.Int(allow_none=True, validate=validate.Range(min=1))

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
    max_iter = fields.Int(allow_none=True, validate=validate.Range(min=1))
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


def validate_search_algorithm(algorithms):
    if sum([1 for f in algorithms if f is not None]) > 1:
        raise ValidationError('Only one search algorithm can be used.')


def validate_matrix(matrix):
    if not matrix:
        return None

    matrix_data = {}
    for key, value in six.iteritems(matrix):
        matrix_data[key] = MatrixConfig.from_dict(value)

    return matrix_data


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

    @validates_schema
    def validate_matrix(self, data):
        """Validates matrix data and creates the config objects"""
        validate_matrix(data.get('matrix'))


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
                 early_stopping=None):
        self.logging = logging
        self.seed = seed
        matrix = validate_matrix(matrix)
        self.matrix = matrix
        self.concurrent_experiments = concurrent_experiments
        validate_search_algorithm([random_search, hyperband])
        self.random_search = random_search
        self.hyperband = hyperband
        self.early_stopping = early_stopping

    def to_dict(self, humanize_values=False):
        results = super(SettingsConfig, self).to_dict(humanize_values=humanize_values)
        if not results.get('matrix'):
            return results
        results['matrix'] = {k: v.to_dict() for k, v in six.iteritems(results['matrix'])}
        return results

    @classmethod
    def get_experiment_settings(cls, data):
        _data = {}
        logging = data.get('logging')
        if logging:
            _data['logging'] = logging
        early_stopping = data.get('early_stopping')
        condition = (
            early_stopping and
            (EarlyStoppingPolicy.stop_experiment(early_stopping) or
             EarlyStoppingPolicy.stop_all(early_stopping)))
        if condition:
            _data['early_stopping'] = early_stopping

        return _data or None
