# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load, validate

from polyaxon_schemas.base import BaseConfig


class BOIterationSchema(Schema):
    iteration = fields.Int()
    experiment_ids = fields.List(fields.Int(), allow_none=True)
    experiment_configs = fields.List(
        fields.List(fields.Raw(), validate=validate.Length(equal=2)),
        allow_none=True)
    experiments_metrics = fields.List(
        fields.List(fields.Raw(), validate=validate.Length(equal=2)),
        allow_none=True)
    new_experiment_ids = fields.List(fields.Int(), allow_none=True)
    new_experiment_configs = fields.List(
        fields.List(fields.Raw(), validate=validate.Length(equal=2)),
        allow_none=True)
    new_experiments_metrics = fields.List(
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
                 experiment_ids=None,
                 experiments_metrics=None,
                 experiment_configs=None,
                 new_experiment_ids=None,
                 new_experiments_metrics=None,
                 new_experiment_configs=None):
        self.iteration = iteration
        self.experiment_ids = experiment_ids
        self.experiment_configs = experiment_configs
        self.experiments_metrics = experiments_metrics
        self.new_experiment_ids = new_experiment_ids
        self.new_experiments_metrics = new_experiments_metrics
        self.new_experiment_configs = new_experiment_configs
