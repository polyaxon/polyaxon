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
from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.logging import LoggingConfig, LoggingSchema
from polyaxon_schemas.matrix import MatrixConfig
from polyaxon_schemas.polyaxonfile.utils import cached_property
from polyaxon_schemas.utils import EarlyStoppingPolicy, Optimization, SearchAlgorithms


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
    n_experiments = fields.Int(validate=validate.Range(min=1))

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


class GridSearchSchema(Schema):
    n_experiments = fields.Int(allow_none=True, validate=validate.Range(min=1))

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return GridSearchConfig(**data)

    @post_dump
    def unmake(self, data):
        return GridSearchConfig.remove_reduced_attrs(data)


class GridSearchConfig(BaseConfig):
    SCHEMA = GridSearchSchema
    IDENTIFIER = 'grid_search'

    def __init__(self, n_experiments=None):
        self.n_experiments = n_experiments


class SearchMetricSchema(Schema):
    name = fields.Str()
    optimization = fields.Str(allow_none=True, validate=validate.OneOf(Optimization.VALUES))

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return SearchMetricConfig(**data)

    @post_dump
    def unmake(self, data):
        return SearchMetricConfig.remove_reduced_attrs(data)


class SearchMetricConfig(BaseConfig):
    SCHEMA = SearchMetricSchema
    IDENTIFIER = 'search_metric'

    def __init__(self,
                 name,
                 optimization=Optimization.MAXIMIZE):
        self.name = name
        self.optimization = optimization


class HyperbandSchema(Schema):
    max_iter = fields.Int(validate=validate.Range(min=1))
    eta = fields.Float(validate=validate.Range(min=0))
    resource = fields.Str()
    metric = fields.Nested(SearchMetricSchema)
    resume = fields.Boolean(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return HyperbandConfig(**data)

    @post_dump
    def unmake(self, data):
        return HyperbandConfig.remove_reduced_attrs(data)


class HyperbandConfig(BaseConfig):
    SCHEMA = HyperbandSchema
    IDENTIFIER = 'hyperband'

    def __init__(self, max_iter, eta, resource, metric, resume=False):
        self.max_iter = max_iter
        self.eta = eta
        self.resource = resource
        self.metric = metric
        self.resume = resume


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
    grid_search = fields.Nested(GridSearchSchema, allow_none=None)
    random_search = fields.Nested(RandomSearchSchema, allow_none=None)
    hyperband = fields.Nested(HyperbandSchema, allow_none=None)
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
        validate_search_algorithm([data.get('grid_search'),
                                   data.get('random_search'),
                                   data.get('hyperband')])

    @validates_schema
    def validate_matrix(self, data):
        """Validates matrix data and creates the config objects"""
        validate_matrix(data.get('matrix'))


class SettingsConfig(BaseConfig):
    SCHEMA = SettingsSchema
    IDENTIFIER = 'settings'
    REDUCED_ATTRIBUTES = ['grid_search', 'random_search', 'hyperband']

    def __init__(self,
                 logging=LoggingConfig(),
                 seed=None,
                 matrix=None,
                 concurrent_experiments=1,
                 grid_search=None,
                 random_search=None,
                 hyperband=None,
                 early_stopping=None):
        self.logging = logging
        self.seed = seed
        matrix = validate_matrix(matrix)
        self.matrix = matrix
        self.concurrent_experiments = concurrent_experiments
        validate_search_algorithm([grid_search, random_search, hyperband])
        self.grid_search = grid_search
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

    @cached_property
    def search_algorithm(self):
        if not self.matrix:
            raise PolyaxonConfigurationError('a search algorithm requires a matrix definition.')
        if self.random_search:
            return SearchAlgorithms.RANDOM
        if self.hyperband:
            return SearchAlgorithms.HYPERBAND
        if self.grid_search:
            return SearchAlgorithms.GRID
        # Default value
        return SearchAlgorithms.GRID
