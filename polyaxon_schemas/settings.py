# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load, validate, post_dump

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.logging import LoggingSchema, LoggingConfig
from polyaxon_schemas.utils import RunTypes, SEARCH_METHODS


class EarlyStoppingMetricSchema(Schema):
    metric = fields.Str()
    value = fields.Float()
    higher = fields.Bool(default=True, allow_none=True)

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
                 higher=True):
        self.metric = metric
        self.value = value
        self.higher = higher


class SettingsSchema(Schema):
    logging = fields.Nested(LoggingSchema, allow_none=True)
    export_strategies = fields.Str(allow_none=True)
    run_type = fields.Str(allow_none=True, validate=validate.OneOf(RunTypes.VALUES))
    concurrent_experiments = fields.Int(allow_none=True)
    search_method = fields.Str(allow_none=True, validate=validate.OneOf(SEARCH_METHODS.VALUES))
    n_experiments = fields.Float(allow_none=True, validate=validate.Range(min=0))
    early_stopping = fields.Nested(EarlyStoppingMetricSchema, many=True, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return SettingsConfig(**data)

    @post_dump
    def unmake(self, data):
        return SettingsConfig.remove_reduced_attrs(data)


class SettingsConfig(BaseConfig):
    SCHEMA = SettingsSchema
    IDENTIFIER = 'settings'

    def __init__(self,
                 logging=LoggingConfig(),
                 export_strategies=None,
                 run_type=RunTypes.KUBERNETES,
                 concurrent_experiments=1,
                 search_method=SEARCH_METHODS.SEQUENTIAL,
                 n_experiments=None,
                 early_stopping=None):
        self.logging = logging
        self.export_strategies = export_strategies
        self.run_type = run_type
        self.concurrent_experiments = concurrent_experiments
        self.search_method = search_method
        self.n_experiments = (int(n_experiments)
                              if (n_experiments and n_experiments >= 1)
                              else n_experiments)
        self.early_stopping = early_stopping
