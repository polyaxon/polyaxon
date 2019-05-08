# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.fields import IntOrStr


class OutputsSchema(BaseSchema):
    jobs = fields.List(IntOrStr(), allow_none=True)
    experiments = fields.List(IntOrStr(), allow_none=True)

    @staticmethod
    def schema_config():
        return OutputsConfig


class OutputsConfig(BaseConfig):
    """
    Outputs config.

    Defines the list of previous jobs/experiments outputs paths
    to make available to other experiments/jobs.

    Args:
        jobs: `list(str)`. The list of the names of jobs to make available for the current run.
        experiments: `list(str)`. The list of the names of experiments
            to make available for the current run.
    """
    IDENTIFIER = 'outputs'
    SCHEMA = OutputsSchema

    def __init__(self, jobs=None, experiments=None):
        self.jobs = jobs
        self.experiments = experiments
