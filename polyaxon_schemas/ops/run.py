# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.ops.build import BuildSchema
from polyaxon_schemas.ops.environments.base import EnvironmentSchema
from polyaxon_schemas.ops.logging import LoggingSchema


class BaseRunSchema(BaseSchema):
    version = fields.Int(allow_none=None)
    kind = fields.Str(allow_none=None, validate=validate.Equal('Implement'))
    logging = fields.Nested(LoggingSchema, allow_none=None)
    tags = fields.List(fields.Str(), allow_none=None)
    environment = fields.Nested(EnvironmentSchema, allow_none=True)
    build = fields.Nested(BuildSchema)

    @staticmethod
    def schema_config():
        return BaseRunConfig


class BaseRunConfig(BaseConfig):
    """
    Build config.

    Args:
        image: str. The name of the image to use during the build step.
        build_steps: list(str). The build steps to apply to your docker image.
            (translate to multiple RUN ...)
        env_vars: list((str, str)) The environment variable to set on you docker image.
        nocache: `bool`. To not use cache when building the image.
        ref: `str`. The commit/branch/treeish to use.

    """
    SCHEMA = BaseRunSchema
    IDENTIFIER = 'run'
    REDUCED_ATTRIBUTES = [
        'kind',
        'version',
        'logging',
        'tags',
        'environment',
    ]

    def __init__(self,
                 kind=None,
                 version=None,
                 logging=None,
                 tags=None,
                 environment=None,
                 build=None,
                 ):
        self.kind = kind
        self.version = version
        self.logging = logging
        self.tags = tags
        self.environment = environment
        self.build = build
