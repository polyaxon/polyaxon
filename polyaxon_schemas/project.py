# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load
from marshmallow import validate

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.experiment import ExperimentSchema
from polyaxon_schemas.utils import UUID


class PolyaxonSpecSchema(Schema):
    uuid = UUID(allow_none=True)
    content = fields.Str()
    project = UUID(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return PolyaxonSpecConfig(**data)


class PolyaxonSpecConfig(BaseConfig):
    SCHEMA = PolyaxonSpecSchema
    IDENTIFIER = 'spec'
    REDUCED_ATTRIBUTES = ['uuid', 'project']

    def __init__(self, content=None, uuid=None, project=None):
        self.content = content
        self.uuid = uuid
        self.project = project


class ProjectSchema(Schema):
    name = fields.Str(validate=validate.Regexp(regex=r'^[-a-zA-Z0-9_]+\Z'))  # TODO: must be slug
    uuid = UUID(allow_none=True)
    description = fields.Str(allow_none=True)
    is_public = fields.Boolean(allow_none=True)
    experiments = fields.Nested(ExperimentSchema, many=True, allow_none=True)
    specs = fields.Nested(PolyaxonSpecSchema, many=True, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ProjectConfig(**data)


class ProjectConfig(BaseConfig):
    SCHEMA = ProjectSchema
    IDENTIFIER = 'project'
    REDUCED_ATTRIBUTES = ['uuid', 'description', 'experiments', 'specs']

    def __init__(self,
                 name,
                 uuid=None,
                 description=None,
                 is_public=True,
                 experiments=None,
                 specs=None):
        self.name = name
        self.uuid = uuid
        self.description = description
        self.is_public = is_public
        self.experiments = experiments
        self.specs = specs
