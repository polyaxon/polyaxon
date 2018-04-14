# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load, validate

from polyaxon_schemas.base import BaseConfig


class HyperbandIterationSchema(Schema):
    iteration = fields.Int()
    bracket_iteration = fields.Int()
    experiment_ids = fields.List(fields.Int())
    experiments_metrics = fields.List(fields.List(fields.Raw(), validate=validate.Length(equal=2)),
                                      allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return HyperbandIterationConfig(**data)

    @post_dump
    def unmake(self, data):
        return HyperbandIterationConfig.remove_reduced_attrs(data)


class HyperbandIterationConfig(BaseConfig):
    SCHEMA = HyperbandIterationSchema

    def __init__(self, iteration, bracket_iteration, experiment_ids, experiments_metrics=None):
        self.iteration = iteration
        self.bracket_iteration = bracket_iteration
        self.experiment_ids = experiment_ids
        self.experiments_metrics = experiments_metrics
