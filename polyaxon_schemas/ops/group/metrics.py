# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.base import BaseConfig, BaseSchema


class Optimization(object):
    MAXIMIZE = 'maximize'
    MINIMIZE = 'minimize'

    MAXIMIZE_VALUES = [MAXIMIZE, MAXIMIZE.upper(), MAXIMIZE.capitalize()]
    MINIMIZE_VALUES = [MINIMIZE, MINIMIZE.upper(), MINIMIZE.capitalize()]

    VALUES = MAXIMIZE_VALUES + MINIMIZE_VALUES

    @classmethod
    def maximize(cls, value):
        return value in cls.MAXIMIZE_VALUES

    @classmethod
    def minimize(cls, value):
        return value in cls.MINIMIZE_VALUES


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
