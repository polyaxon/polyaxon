# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import ast
import copy
import numpy as np
import six

from collections import Mapping

from marshmallow import fields, validates_schema
from marshmallow.exceptions import ValidationError

from polyaxon_schemas.base import BaseConfig, BaseSchema

# pylint:disable=redefined-outer-name


class PValue(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, (list, tuple)) and len(value) == 2:
            if isinstance(value[1], float) and 0 <= value[1] < 1:
                return value
        raise ValidationError("This field expects a list of [value<Any>, dist<float>].")


class Range(fields.Field):
    REQUIRED_KEYS = ['start', 'stop', 'step']
    OPTIONAL_KEY = None
    KEYS = REQUIRED_KEYS

    def _deserialize(self, value, attr, data, **kwargs):  # pylint:disable=too-many-branches
        if isinstance(value, six.string_types):
            value = value.split(':')
        elif isinstance(value, Mapping):
            if set(self.REQUIRED_KEYS) - set(six.iterkeys(value)):
                raise ValidationError("{} dict must have {} keys {}.".format(
                    self.__class__.__name__, len(self.REQUIRED_KEYS), self.REQUIRED_KEYS))
            if len(value) == len(self.REQUIRED_KEYS):
                value = [value[k] for k in self.REQUIRED_KEYS]
            elif len(value) == len(self.KEYS):
                value = [value[k] for k in self.KEYS]
        elif not isinstance(value, list):
            raise ValidationError(
                "{} accept values formatted as the following:\n"
                " * str: {}\n"
                " * dict: {}\n"
                " * list: {}".format(
                    self.__class__.__name__,
                    ':'.join(self.REQUIRED_KEYS),
                    dict(zip(self.REQUIRED_KEYS,
                             ['v{}'.format(i) for i in range(len(self.REQUIRED_KEYS))])),
                    self.REQUIRED_KEYS))

        if len(value) != len(self.REQUIRED_KEYS) and len(value) != len(self.KEYS):
            raise ValidationError("{} requires {} or {} elements received {}".format(
                self.__class__.__name__,
                len(self.REQUIRED_KEYS),
                len(self.KEYS),
                len(value)))

        for i, v in enumerate(value):
            try:
                float(v)
            except (ValueError, TypeError):
                raise ValidationError(
                    "{}: {} must of type int or float, received instead {}".format(
                        self.__class__.__name__, self.REQUIRED_KEYS[i], v
                    ))
            if not isinstance(v, (int, float)):
                value[i] = ast.literal_eval(v)

        # Check that lower value is  smaller than higher value
        if value[0] >= value[1]:
            raise ValidationError(
                "{key2} value must strictly higher that {key1} value, "
                "received instead {key1}: {val1}, {key2}: {val2}".format(
                    key1=self.REQUIRED_KEYS[0],
                    key2=self.REQUIRED_KEYS[1],
                    val1=value[0],
                    val2=value[1]))
        if len(self.REQUIRED_KEYS) == 3 and value[2] == 0:
            raise ValidationError("{} cannot be 0".format(self.REQUIRED_KEYS[2]))

        value = dict(zip(self.KEYS, value))
        return value


class LinSpace(Range):
    REQUIRED_KEYS = ['start', 'stop', 'num']
    KEYS = REQUIRED_KEYS


class GeomSpace(Range):
    REQUIRED_KEYS = ['start', 'stop', 'num']
    KEYS = REQUIRED_KEYS


class LogSpace(Range):
    REQUIRED_KEYS = ['start', 'stop', 'num']
    OPTIONAL_KEYS = ['base']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


def uniform(low, high, size=None, rand_generator=None):
    rand_generator = rand_generator or np.random
    return rand_generator.uniform(low=low, high=high, size=size)


def quniform(low, high, q, size=None, rand_generator=None):
    value = uniform(low=low, high=high, size=size, rand_generator=rand_generator)
    return np.round(value // q) * q


def loguniform(low, high, size=None, rand_generator=None):
    value = uniform(low=low, high=high, size=size, rand_generator=rand_generator)
    return np.exp(value)


def qloguniform(low, high, q, size=None, rand_generator=None):
    value = loguniform(low=low, high=high, size=size, rand_generator=rand_generator)
    return np.round(value // q) * q


def normal(loc, scale, size=None, rand_generator=None):
    rand_generator = rand_generator or np.random
    return rand_generator.normal(loc=loc, scale=scale, size=size)


def qnormal(loc, scale, q, size=None, rand_generator=None):
    draw = normal(loc=loc, scale=scale, size=size, rand_generator=rand_generator)
    return np.round(draw // q) * q


def lognormal(loc, scale, size=None, rand_generator=None):
    rand_generator = rand_generator or np.random
    return rand_generator.lognormal(mean=loc, sigma=scale, size=size)


def qlognormal(loc, scale, q, size=None, rand_generator=None):
    draw = lognormal(loc=loc, scale=scale, size=size, rand_generator=rand_generator)
    return np.exp(draw)


def validate_pvalues(values):
    dists = [v for v in values if v]
    if sum(dists) > 1:
        raise ValidationError('The distribution of different outcomes should sum to 1.')


def pvalues(values, size=None, rand_generator=None):
    rand_generator = rand_generator or np.random
    keys = [v[0] for v in values]
    dists = [v[1] for v in values]
    validate_pvalues(dists)
    indices = rand_generator.multinomial(1, dists, size=size)
    if size is None:
        return keys[indices.argmax()]
    return [keys[ind.argmax()] for ind in indices]


class Uniform(Range):
    REQUIRED_KEYS = ['low', 'high']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class QUniform(Range):
    REQUIRED_KEYS = ['low', 'high', 'q']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class LogUniform(Range):
    REQUIRED_KEYS = ['low', 'high']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class QLogUniform(Range):
    REQUIRED_KEYS = ['low', 'high', 'q']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class Normal(Range):
    REQUIRED_KEYS = ['loc', 'scale']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class QNormal(Range):
    REQUIRED_KEYS = ['loc', 'scale', 'q']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class LogNormal(Range):
    REQUIRED_KEYS = ['loc', 'scale']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class QLogNormal(Range):
    REQUIRED_KEYS = ['loc', 'scale', 'q']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


def validate_matrix(values):
    v = sum(map(lambda x: 1 if x else 0, values))
    if v == 0 or v > 1:
        raise ValidationError("Matrix element is not valid, one and only one option is required.")


class MatrixSchema(BaseSchema):
    # Discrete
    values = fields.List(fields.Raw(), allow_none=True)
    pvalues = fields.List(PValue(), allow_none=True)
    range = Range(allow_none=True)
    linspace = LinSpace(allow_none=True)
    logspace = LogSpace(allow_none=True)
    geomspace = GeomSpace(allow_none=True)
    # Continuous
    uniform = Uniform(allow_none=True)
    quniform = QUniform(allow_none=True)
    loguniform = LogUniform(allow_none=True)
    qloguniform = QLogUniform(allow_none=True)
    normal = Normal(allow_none=True)
    qnormal = QNormal(allow_none=True)
    lognormal = LogNormal(allow_none=True)
    qlognormal = QLogNormal(allow_none=True)

    @staticmethod
    def schema_config():
        return MatrixConfig

    @validates_schema
    def validate_pvalues(self, data):
        if data.get('pvalues'):
            validate_pvalues(values=[v[1] for v in data['pvalues'] if v])

    @validates_schema
    def validate_matrix(self, data):
        validate_matrix([
            data.get('values'),
            data.get('pvalues'),
            data.get('range'),
            data.get('linspace'),
            data.get('logspace'),
            data.get('geomspace'),
            data.get('uniform'),
            data.get('quniform'),
            data.get('loguniform'),
            data.get('qloguniform'),
            data.get('normal'),
            data.get('qnormal'),
            data.get('lognormal'),
            data.get('qlognormal'),
        ])


class MatrixConfig(BaseConfig):
    IDENTIFIER = 'matrix'
    SCHEMA = MatrixSchema
    REDUCED_ATTRIBUTES = [
        'values', 'pvalues', 'range', 'linspace', 'logspace', 'geomspace',
        'uniform', 'quniform', 'loguniform', 'qloguniform',
        'normal', 'qnormal', 'lognormal', 'qlognormal'
    ]

    NUMPY_MAPPING = {
        'range': np.arange,
        'linspace': np.linspace,
        'logspace': np.logspace,
        'geomspace': np.geomspace,
        'uniform': uniform,
        'quniform': quniform,
        'loguniform': loguniform,
        'qloguniform': qloguniform,
        'normal': normal,
        'qnormal': qnormal,
        'lognormal': lognormal,
        'qlognormal': qlognormal,
    }

    RANGES = {
        'range', 'linspace', 'logspace', 'geomspace'
    }

    CONTINUOUS = {
        'uniform', 'quniform', 'loguniform', 'qloguniform',
        'normal', 'qnormal', 'lognormal', 'qlognormal'
    }

    DISTRIBUTIONS = {
        'pvalues',
        'uniform', 'quniform', 'loguniform', 'qloguniform',
        'normal', 'qnormal', 'lognormal', 'qlognormal'
    }

    def __init__(self,
                 values=None,
                 pvalues=None,
                 range=None,  # noqa
                 linspace=None,
                 logspace=None,
                 geomspace=None,
                 uniform=None,
                 quniform=None,
                 loguniform=None,
                 qloguniform=None,
                 normal=None,
                 qnormal=None,
                 lognormal=None,
                 qlognormal=None):
        self.values = values
        self.pvalues = pvalues
        self.range = range
        self.linspace = linspace
        self.logspace = logspace
        self.geomspace = geomspace
        self.uniform = uniform
        self.quniform = quniform
        self.loguniform = loguniform
        self.qloguniform = qloguniform
        self.normal = normal
        self.qnormal = qnormal
        self.lognormal = lognormal
        self.qlognormal = qlognormal

        validate_matrix([
            values, pvalues, range, linspace, logspace, geomspace, uniform, quniform,
            loguniform, qloguniform, normal, qnormal, lognormal, qlognormal])

    @property
    def is_distribution(self):
        key = list(six.iterkeys(self.to_dict()))[0]
        return key in self.DISTRIBUTIONS

    @property
    def is_continuous(self):
        key = list(six.iterkeys(self.to_dict()))[0]
        return key in self.CONTINUOUS

    @property
    def is_discrete(self):
        return not self.is_continuous

    @property
    def is_range(self):
        key = list(six.iterkeys(self.to_dict()))[0]
        return key in self.RANGES

    @property
    def is_categorical(self):
        key, value = list(six.iteritems(self.to_dict()))[0]
        if key != 'values':
            return False

        return any([v for v in value
                    if not isinstance(v, (int, float, complex, np.integer, np.floating))])

    @property
    def is_uniform(self):
        key = list(six.iterkeys(self.to_dict()))[0]
        return key == 'uniform'

    @property
    def min(self):
        if self.is_categorical:
            return None

        if self.is_range:
            value = list(six.itervalues(self.to_dict()))[0]
            return value.get('start')

        if self.is_discrete and not self.is_distribution:
            return min(self.to_numpy())

        if self.is_uniform:
            value = list(six.itervalues(self.to_dict()))[0]
            return value.get('low')

        return None

    @property
    def max(self):
        if self.is_categorical:
            return None

        if self.is_range:
            value = list(six.itervalues(self.to_dict()))[0]
            return value.get('stop')

        if self.is_discrete and not self.is_distribution:
            return max(self.to_numpy())

        if self.is_uniform:
            value = list(six.itervalues(self.to_dict()))[0]
            return value.get('high')

        return None

    @property
    def length(self):
        key, value = list(six.iteritems(self.to_dict()))[0]
        if key in ['values', 'pvalues']:
            return len(value)

        if key in self.DISTRIBUTIONS:
            raise ValidationError('Distribution should not call `to_numpy`, '
                                  'instead it should call `sample`.')

        return len(self.NUMPY_MAPPING[key](**value))

    def to_numpy(self):
        key, value = list(six.iteritems(self.to_dict()))[0]
        if key == 'values':
            return value

        if key in self.DISTRIBUTIONS:
            raise ValidationError('Distribution should not call `to_numpy`, '
                                  'instead it should call `sample`.')

        return self.NUMPY_MAPPING[key](**value)

    def sample(self, size=None, rand_generator=None):
        size = None if size == 1 else size
        key, value = list(six.iteritems(self.to_dict()))[0]
        value = copy.deepcopy(value)
        if key in {'values', 'range', 'linspace', 'logspace', 'geomspace'}:
            value = self.to_numpy()
            rand_generator = rand_generator or np.random
            try:
                return rand_generator.choice(value, size=size)
            except ValueError:
                idx = rand_generator.randint(0, len(value))
                return value[idx]

        if key == 'pvalues':
            return pvalues(values=value, size=size, rand_generator=rand_generator)

        value['size'] = size
        value['rand_generator'] = rand_generator
        return self.NUMPY_MAPPING[key](**value)
