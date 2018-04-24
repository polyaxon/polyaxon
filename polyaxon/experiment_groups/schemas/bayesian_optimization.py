# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load, validate

from polyaxon_schemas.base import BaseConfig


class BOIterationSchema(Schema):
    iteration = fields.Int()
    old_experiment_ids = fields.List(fields.Int(), allow_none=True)
    old_experiments_configs = fields.List(
        fields.List(fields.Raw(), validate=validate.Length(equal=2)),
        allow_none=True)
    old_experiments_metrics = fields.List(
        fields.List(fields.Raw(), validate=validate.Length(equal=2)),
        allow_none=True)
    experiment_ids = fields.List(fields.Int(), allow_none=True)
    experiments_configs = fields.List(
        fields.List(fields.Raw(), validate=validate.Length(equal=2)),
        allow_none=True)
    experiments_metrics = fields.List(
        fields.List(fields.Raw(), validate=validate.Length(equal=2)),
        allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return BOIterationConfig(**data)

    @post_dump
    def unmake(self, data):
        return BOIterationConfig.remove_reduced_attrs(data)


class BOIterationConfig(BaseConfig):
    SCHEMA = BOIterationSchema

    def __init__(self,
                 iteration,
                 old_experiment_ids=None,
                 old_experiments_metrics=None,
                 old_experiments_configs=None,
                 experiment_ids=None,
                 experiments_metrics=None,
                 experiments_configs=None):
        self.iteration = iteration
        self.old_experiment_ids = old_experiment_ids
        self.old_experiments_metrics = old_experiments_metrics
        self.old_experiments_configs = old_experiments_configs
        self.experiment_ids = experiment_ids
        self.experiments_configs = experiments_configs
        self.experiments_metrics = experiments_metrics

    @property
    def combined_experiment_ids(self):
        experiment_ids = self.old_experiment_ids or []
        experiment_ids += self.experiment_ids or []
        return experiment_ids

    @property
    def combined_experiments_configs(self):
        experiments_configs = self.old_experiments_configs or []
        experiments_configs += self.experiments_configs or []
        return experiments_configs

    @property
    def combined_experiments_metrics(self):
        experiments_metrics = self.old_experiments_metrics or []
        experiments_metrics += self.experiments_metrics or []
        return experiments_metrics
