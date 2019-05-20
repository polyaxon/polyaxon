# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.ops.run import BaseRunConfig, BaseRunSchema, RunSchema


class JobSchema(BaseRunSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal('job'))
    run = fields.Nested(RunSchema, allow_none=True)
    backend = fields.Str(allow_none=True)
    framework = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return JobConfig


class JobConfig(BaseRunConfig):
    SCHEMA = JobSchema
    IDENTIFIER = 'job'
    REDUCED_ATTRIBUTES = BaseRunConfig.REDUCED_ATTRIBUTES + ['backend', 'framework', 'run']

    def __init__(self,
                 version=None,
                 kind=None,
                 logging=None,
                 name=None,
                 description=None,
                 tags=None,
                 environment=None,
                 params=None,
                 declarations=None,
                 inputs=None,
                 outputs=None,
                 build=None,
                 backend=None,
                 framework=None,
                 run=None,
                 ):
        super(JobConfig, self).__init__(
            version=version,
            kind=kind,
            logging=logging,
            name=name,
            description=description,
            tags=tags,
            environment=environment,
            params=params,
            declarations=declarations,
            inputs=inputs,
            outputs=outputs,
            build=build
        )

        self.run = run
        self.backend = backend
        self.framework = framework
