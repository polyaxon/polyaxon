# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy
import numpy as np
import six

from marshmallow import Schema, fields, post_dump, post_load, validates_schema
from marshmallow.exceptions import ValidationError

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.utils import (
    GeomSpace,
    LinSpace,
    LogNormal,
    LogSpace,
    LogUniform,
    Normal,
    PValue,
    QLogNormal,
    QLogUniform,
    QNormal,
    QUniform,
    Range,
    Uniform,
    lognormal,
    loguniform,
    normal,
    pvalues,
    qlognormal,
    qloguniform,
    qnormal,
    quniform,
    uniform,
    validate_pvalues
)

# pylint:disable=redefined-outer-name


def validate_matrix(values):
    v = sum(map(lambda x: 1 if x else 0, values))
    if v == 0 or v > 1:
        raise ValidationError("Matrix element is not valid, one and only one option is required.")


class MatrixSchema(Schema):
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

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return MatrixConfig(**data)

    @post_dump
    def unmake(self, data):
        return MatrixConfig.remove_reduced_attrs(data)

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
    def is_discrete(self):
        return not self.is_distribution

    @property
    def is_range(self):
        key = list(six.iterkeys(self.to_dict()))[0]
        return key in self.RANGES

    @property
    def is_categorical(self):
        key, value = list(six.iteritems(self.to_dict()))[0]
        if key != 'values':
            return False

        return any([v for v in value if isinstance(v, six.string_types)])

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

        if self.is_discrete:
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

        if self.is_discrete:
            return max(self.to_numpy())

        if self.is_uniform:
            value = list(six.itervalues(self.to_dict()))[0]
            return value.get('high')

        return None

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
            return rand_generator.choice(value, size=size)

        if key == 'pvalues':
            return pvalues(values=value, size=size, rand_generator=rand_generator)

        value['size'] = size
        value['rand_generator'] = rand_generator
        return self.NUMPY_MAPPING[key](**value)
