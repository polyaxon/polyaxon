# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.ops.run import BaseRunConfig, BaseRunSchema, RunSchema


class JobSchema(BaseRunSchema):
    kind = fields.Str(allow_none=None, validate=validate.Equal('job'))
    declarations = fields.Raw(allow_none=True)
    run = fields.Nested(RunSchema, allow_none=True)
    backend = fields.Str(allow_none=True)
    framework = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return JobConfig


class JobConfig(BaseRunConfig):
    SCHEMA = JobSchema
    IDENTIFIER = 'job'

    def __init__(self,
                 kind=None,
                 version=None,
                 logging=None,
                 tags=None,
                 declarations=None,
                 environment=None,
                 build=None,
                 run=None,
                 backend=None,
                 framework=None):
        super(JobConfig, self).__init__(kind=kind,
                                        version=version,
                                        logging=logging,
                                        tags=tags,
                                        environment=environment,
                                        build=build)

        self.declarations = declarations
        self.run = run
        self.backend = backend
        self.framework = framework
