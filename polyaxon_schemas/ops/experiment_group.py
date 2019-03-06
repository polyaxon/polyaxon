# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.ops.experiment import ExperimentConfig, ExperimentSchema
from polyaxon_schemas.ops.hptuning import HPTuningSchema
from polyaxon_schemas.ops.run import BaseRunConfig


class ExperimentGroupSchema(ExperimentSchema):
    hptuning = fields.Nested(HPTuningSchema, allow_none=None)

    @staticmethod
    def schema_config():
        return ExperimentGroupConfig


class ExperimentGroupConfig(ExperimentConfig):
    SCHEMA = ExperimentSchema
    IDENTIFIER = 'experiment'
    REDUCED_ATTRIBUTES = BaseRunConfig.REDUCED_ATTRIBUTES + ['backend', 'framework']

    def __init__(self,
                 kind=None,
                 version=None,
                 logging=None,
                 tags=None,
                 declarations=None,
                 hptuning=None,
                 environment=None,
                 build=None,
                 backend=None,
                 framework=None,
                 run=None,
                 model=None,
                 train=None,
                 eval=None,  # pylint:disable=redefined-builtin
                 ):
        super(ExperimentGroupConfig, self).__init__(
            kind=kind,
            version=version,
            logging=logging,
            tags=tags,
            declarations=declarations,
            environment=environment,
            build=build,
            backend=backend,
            framework=framework,
            run=run,
            model=model,
            train=train,
            eval=eval)
        self.hptuning = hptuning
