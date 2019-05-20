# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.ops.build_job import BuildSchema
from polyaxon_schemas.ops.operation import BaseOpConfig, BaseOpSchema


class BaseRunSchema(BaseOpSchema):
    build = fields.Nested(BuildSchema)

    @staticmethod
    def schema_config():
        return BaseRunConfig


class BaseRunConfig(BaseOpConfig):
    SCHEMA = BaseRunSchema
    IDENTIFIER = 'run'
    REDUCED_ATTRIBUTES = BaseOpConfig.REDUCED_ATTRIBUTES + ['build']

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
                 ):
        super(BaseRunConfig, self).__init__(
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
        )
        self.build = build
