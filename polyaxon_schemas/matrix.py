# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np
import six

from marshmallow import Schema, fields, post_load, post_dump

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.utils import Range, LinSpace, GeomSpace, LogSpace


class MatrixSchema(Schema):
    values = fields.List(fields.Raw(), allow_none=True)
    range = Range(allow_none=True)
    linspace = LinSpace(allow_none=True)
    logspace = LogSpace(allow_none=True)
    geomspace = GeomSpace(allow_none=True)

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
    REDUCED_ATTRIBUTES = ['values', 'range', 'linspace', 'logspace', 'geomspace']

    NUMPY_MAPPING = {
        'range': np.arange,
        'linspace': np.linspace,
        'logspace': np.logspace,
        'geomspace': np.geomspace
    }

    def __init__(self, values=None, range=None, linspace=None, logspace=None, geomspace=None):
        self.values = values
        self.range = range
        self.linspace = linspace
        self.logspace = logspace
        self.geomspace = geomspace

        v = sum(map(lambda x: 1 if x else 0, [values, range, linspace, logspace, geomspace]))
        if v == 0 or v > 1:
            raise ValueError("Matrix element is not valid, one and only one option is required.")

    def to_numpy(self):
        key, value = list(six.iteritems(self.to_dict()))[0]
        if key == 'values':
            return value

        return self.NUMPY_MAPPING[key](**value)
