# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.ops.experiment import ExperimentConfig, ExperimentSchema
from polyaxon_schemas.ops.group.hptuning import HPTuningSchema


class GroupSchema(ExperimentSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal('group'))
    hptuning = fields.Nested(HPTuningSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return GroupConfig


class GroupConfig(ExperimentConfig):
    SCHEMA = GroupSchema
    IDENTIFIER = 'group'
    REDUCED_ATTRIBUTES = ExperimentConfig.REDUCED_ATTRIBUTES + ['hptuning']

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
                 hptuning=None,
                 ):
        super(GroupConfig, self).__init__(
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
            build=build,
            backend=backend,
            framework=framework,
            run=run,
        )
        self.hptuning = hptuning
