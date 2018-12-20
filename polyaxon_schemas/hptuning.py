# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.matrix import MatrixConfig
from polyaxon_schemas.polyaxonfile.utils import cached_property
from polyaxon_schemas.utils import (
    AcquisitionFunctions,
    EarlyStoppingPolicy,
    GaussianProcessesKernels,
    Optimization,
    ResourceTypes,
    SearchAlgorithms
)


class EarlyStoppingMetricSchema(BaseSchema):
    metric = fields.Str()
    value = fields.Float()
    optimization = fields.Str(allow_none=True, validate=validate.OneOf(Optimization.VALUES))
    policy = fields.Str(allow_none=True, validate=validate.OneOf(EarlyStoppingPolicy.VALUES))

    @staticmethod
    def schema_config():
        return EarlyStoppingMetricConfig


class EarlyStoppingMetricConfig(BaseConfig):
    """
    Early stopping metric config.

    Args:
        metric: `str`. The metric to use for early stopping.
        value: `float`. The metric value to use for the condition.
        optimization: `string`. The optimization to do: maximize or minimize.
    """
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


class RandomSearchSchema(BaseSchema):
    n_experiments = fields.Int(allow_none=True, validate=validate.Range(min=1))

    @staticmethod
    def schema_config():
        return RandomSearchConfig


class RandomSearchConfig(BaseConfig):
    SCHEMA = RandomSearchSchema
    IDENTIFIER = 'random_search'
    REDUCED_ATTRIBUTES = ['n_experiments']

    def __init__(self, n_experiments=None):
        self.n_experiments = n_experiments


class GridSearchSchema(BaseSchema):
    n_experiments = fields.Int(allow_none=True, validate=validate.Range(min=1))

    @staticmethod
    def schema_config():
        return GridSearchConfig


class GridSearchConfig(BaseConfig):
    SCHEMA = GridSearchSchema
    IDENTIFIER = 'grid_search'
    REDUCED_ATTRIBUTES = ['n_experiments']

    def __init__(self, n_experiments=None):
        self.n_experiments = n_experiments


class SearchMetricSchema(BaseSchema):
    name = fields.Str()
    optimization = fields.Str(allow_none=True, validate=validate.OneOf(Optimization.VALUES))

    @staticmethod
    def schema_config():
        return SearchMetricConfig


class SearchMetricConfig(BaseConfig):
    SCHEMA = SearchMetricSchema
    IDENTIFIER = 'search_metric'

    def __init__(self,
                 name,
                 optimization=Optimization.MAXIMIZE):
        self.name = name
        self.optimization = optimization


class ResourceSchema(BaseSchema):
    name = fields.Str()
    type = fields.Str(allow_none=True, validate=validate.OneOf(ResourceTypes.VALUES))

    @staticmethod
    def schema_config():
        return ResourceConfig


class ResourceConfig(BaseConfig):
    SCHEMA = ResourceSchema
    IDENTIFIER = 'resource'

    def __init__(self,
                 name,
                 type=ResourceTypes.FLOAT):  # noqa, redefined-builtin `len`
        self.name = name
        self.type = type

    def cast_value(self, value):
        if ResourceTypes.is_int(self.type):
            return int(value)
        if ResourceTypes.is_float(self.type):
            return float(value)
        return value


class HyperbandSchema(BaseSchema):
    max_iter = fields.Int(validate=validate.Range(min=1))
    eta = fields.Float(validate=validate.Range(min=0))
    resource = fields.Nested(ResourceSchema)
    metric = fields.Nested(SearchMetricSchema)
    resume = fields.Boolean(allow_none=True)

    @staticmethod
    def schema_config():
        return HyperbandConfig


class HyperbandConfig(BaseConfig):
    SCHEMA = HyperbandSchema
    IDENTIFIER = 'hyperband'

    def __init__(self, max_iter, eta, resource, metric, resume=False):
        self.max_iter = max_iter
        self.eta = eta
        self.resource = resource
        self.metric = metric
        self.resume = resume


class GaussianProcessSchema(BaseSchema):
    kernel = fields.Str(allow_none=True, validate=validate.OneOf(GaussianProcessesKernels.VALUES))
    length_scale = fields.Float(allow_none=True)
    nu = fields.Float(allow_none=True)
    n_restarts_optimizer = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return GaussianProcessConfig


class GaussianProcessConfig(BaseConfig):
    SCHEMA = GaussianProcessSchema
    IDENTIFIER = 'gaussian_process'

    def __init__(self,
                 kernel=GaussianProcessesKernels.MATERN,
                 length_scale=1.0,
                 nu=1.5,
                 n_restarts_optimizer=0):
        self.kernel = kernel
        self.length_scale = length_scale
        self.nu = nu
        self.n_restarts_optimizer = n_restarts_optimizer


def validate_utility_function(acquisition_function, kappa, eps):
    condition = AcquisitionFunctions.is_ucb(acquisition_function) and kappa is None
    if condition:
        raise ValidationError('the acquisition function `ucb` requires a parameter `kappa`')

    condition = ((AcquisitionFunctions.is_ei(acquisition_function) or
                  AcquisitionFunctions.is_poi(acquisition_function)) and
                 eps is None)
    if condition:
        raise ValidationError('the acquisition function `{}` requires a parameter `eps`'.format(
            acquisition_function
        ))


class UtilityFunctionSchema(BaseSchema):
    acquisition_function = fields.Str(allow_none=True,
                                      validate=validate.OneOf(AcquisitionFunctions.VALUES))
    gaussian_process = fields.Nested(GaussianProcessSchema, allow_none=True)
    kappa = fields.Float(allow_none=True)
    eps = fields.Float(allow_none=True)
    n_warmup = fields.Int(allow_none=True)
    n_iter = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return UtilityFunctionConfig

    @validates_schema
    def validate_utility_function(self, data):
        validate_utility_function(
            acquisition_function=data.get('acquisition_function'),
            kappa=data.get('kappa'),
            eps=data.get('eps'))


class UtilityFunctionConfig(BaseConfig):
    SCHEMA = UtilityFunctionSchema
    IDENTIFIER = 'utility_function'
    REDUCED_ATTRIBUTES = ['n_warmup', 'n_iter']

    def __init__(self,
                 acquisition_function=AcquisitionFunctions.UCB,
                 gaussian_process=None,
                 kappa=None,
                 eps=None,
                 n_warmup=None,
                 n_iter=None):
        validate_utility_function(
            acquisition_function=acquisition_function,
            kappa=kappa,
            eps=eps)

        self.acquisition_function = acquisition_function
        self.gaussian_process = gaussian_process
        self.kappa = kappa
        self.eps = eps
        self.n_warmup = n_warmup
        self.n_iter = n_iter


class BOSchema(BaseSchema):
    utility_function = fields.Nested(UtilityFunctionSchema, allow_none=True)
    n_initial_trials = fields.Int()
    n_iterations = fields.Int()
    metric = fields.Nested(SearchMetricSchema)

    @staticmethod
    def schema_config():
        return BOConfig


class BOConfig(BaseConfig):
    SCHEMA = BOSchema
    IDENTIFIER = 'bo'

    def __init__(self, n_initial_trials, n_iterations, metric, utility_function=None):
        self.n_initial_trials = n_initial_trials
        self.n_iterations = n_iterations
        self.utility_function = utility_function
        self.metric = metric


def validate_search_algorithm(algorithms, matrix):
    used_algorithms = sum([1 for f in algorithms if f is not None])
    if used_algorithms > 1:
        raise ValidationError('Only one search algorithm can be used.')
    if used_algorithms and not matrix:
        raise ValidationError('Search algorithms need a matrix definition.')


def validate_bo_matrix(matrix):
    if not matrix:
        return None

    matrix_data = {}
    for key, value in six.iteritems(matrix):
        if not isinstance(value, MatrixConfig):
            matrix_data[key] = MatrixConfig.from_dict(value)
        else:
            matrix_data[key] = value

        if matrix_data[key].is_distribution and not matrix_data[key].is_uniform:
            raise ValidationError('`{}` defines a non uniform distribution, '
                                  'and it cannot be used with bayesian optimization.'.format(key))

    return matrix_data


def validate_matrix(matrix, is_grid_search=False, is_bo=False):
    if not matrix:
        return None

    matrix_data = {}
    for key, value in six.iteritems(matrix):
        if not isinstance(value, MatrixConfig):
            matrix_data[key] = MatrixConfig.from_dict(value)
        else:
            matrix_data[key] = value

        if is_grid_search and matrix_data[key].is_distribution:
            raise ValidationError('`{}` defines a distribution, '
                                  'and it cannot be used with grid search.'.format(key))

        if is_bo and matrix_data[key].is_distribution and not matrix_data[key].is_uniform:
            raise ValidationError('`{}` defines a non uniform distribution, '
                                  'and it cannot be used with bayesian optimization.'.format(key))

    return matrix_data


class HPTuningSchema(BaseSchema):
    seed = fields.Int(allow_none=True)
    matrix = fields.Dict(allow_none=True)
    concurrency = fields.Int(allow_none=True)
    grid_search = fields.Nested(GridSearchSchema, allow_none=None)
    random_search = fields.Nested(RandomSearchSchema, allow_none=None)
    hyperband = fields.Nested(HyperbandSchema, allow_none=None)
    bo = fields.Nested(BOSchema, allow_none=None)
    early_stopping = fields.Nested(EarlyStoppingMetricSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return HPTuningConfig

    @validates_schema
    def validate_search_algorithm(self, data):
        validate_search_algorithm(
            algorithms=[data.get('grid_search'),
                        data.get('random_search'),
                        data.get('hyperband'),
                        data.get('bo')],
            matrix=data.get('matrix'))

    @validates_schema
    def validate_matrix(self, data):
        """Validates matrix data and creates the config objects"""
        is_grid_search = data.get('grid_search') is not None
        is_bo = data.get('bo') is not None
        validate_matrix(data.get('matrix'), is_grid_search=is_grid_search, is_bo=is_bo)


class HPTuningConfig(BaseConfig):
    SCHEMA = HPTuningSchema
    IDENTIFIER = 'hptuning'
    REDUCED_ATTRIBUTES = ['grid_search', 'random_search', 'hyperband', 'bo']

    def __init__(self,
                 seed=None,
                 matrix=None,
                 concurrency=1,
                 grid_search=None,
                 random_search=None,
                 hyperband=None,
                 bo=None,
                 early_stopping=None):
        self.seed = seed
        matrix = validate_matrix(matrix,
                                 is_grid_search=grid_search is not None,
                                 is_bo=bo is not None)
        self.matrix = matrix
        self.concurrency = concurrency
        validate_search_algorithm(
            algorithms=[grid_search, random_search, hyperband, bo],
            matrix=matrix)
        self.grid_search = grid_search
        self.random_search = random_search
        self.hyperband = hyperband
        self.bo = bo
        self.early_stopping = early_stopping

    def to_dict(self, humanize_values=False):
        results = super(HPTuningConfig, self).to_dict(humanize_values=humanize_values)
        if not results.get('matrix'):
            return results
        results['matrix'] = {k: v.to_dict() for k, v in six.iteritems(results['matrix'])}
        return results

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
        if self.bo:
            return SearchAlgorithms.BO
        # Default value
        return SearchAlgorithms.GRID
