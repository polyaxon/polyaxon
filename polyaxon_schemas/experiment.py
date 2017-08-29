# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

from polyaxon_schemas.base import BaseConfig


class ExperimentSchema(Schema):
    name = fields.Str()
    uuid = fields.UUID()
    project = fields.UUID()
    description = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ExperimentConfig(**data)


class ExperimentConfig(BaseConfig):
    SCHEMA = ExperimentSchema
    IDENTIFIER = 'Experiment'
    REDUCED_ATTRIBUTES = ['description']

    def __init__(self, name, uuid, project, description=None):
        self.name = name
        self.uuid = uuid
        self.project = project
        self.description = description
