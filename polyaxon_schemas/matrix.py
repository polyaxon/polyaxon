# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np
import six

from marshmallow import Schema, fields, post_load, post_dump
from numpy.random.mtrand import normal

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.utils import (
    Range,
    LinSpace,
    GeomSpace,
    LogSpace,
    Uniform,
    QUniform,
    LogUniform,
    QLogUniform,
    Normal,
    QNormal,
    LogNormal,
    QLogNormal,
    quniform,
    loguniform,
    qloguniform,
    lognormal,
    qnormal,
    qlognormal,
    PValue,
    pvalues)


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
        'uniform': np.random.uniform(),
        'quniform': quniform,
        'loguniform': loguniform,
        'qloguniform': qloguniform,
        'normal': normal,
        'qnormal': qnormal,
        'lognormal': lognormal,
        'qlognormal': qlognormal,
    }

    def __init__(self,
                 values=None,
                 pvalues=None,
                 range=None,
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

        v = sum(map(lambda x: 1 if x else 0,
                    [values, pvalues, range, linspace, logspace, geomspace, uniform, quniform,
                     loguniform, qloguniform, normal, qnormal, lognormal, qlognormal]))
        if v == 0 or v > 1:
            raise ValueError("Matrix element is not valid, one and only one option is required.")

    def to_numpy(self):
        key, value = list(six.iteritems(self.to_dict()))[0]
        if key == 'values':
            return value
        if key == 'pvalues':
            return pvalues(pvalues=value)

        return self.NUMPY_MAPPING[key](**value)
