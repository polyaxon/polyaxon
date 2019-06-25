# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

from hestia.cached_property import cached_property
from marshmallow import EXCLUDE

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.ops.job import JobConfig
from polyaxon_schemas.ops.run import RunConfig
from polyaxon_schemas.specs import kinds
from polyaxon_schemas.specs.base import BaseRunSpecification, BaseSpecification


class JobSpecification(BaseRunSpecification):
    """The polyaxonfile specification for run jobs.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        LOGGING: defines the logging
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
        BUILD: defines the build step where the user can set a docker image definition
        RUN: defines the run step where the user can run a command
    """
    _SPEC_KIND = kinds.JOB

    REQUIRED_SECTIONS = BaseRunSpecification.REQUIRED_SECTIONS + (
        BaseSpecification.BUILD, BaseSpecification.RUN,
    )

    POSSIBLE_SECTIONS = BaseRunSpecification.POSSIBLE_SECTIONS + (
        BaseRunSpecification.PARAMS,
        BaseRunSpecification.RUN,
    )

    CONFIG = JobConfig

    @cached_property
    def run(self):
        return self.config.run

    @classmethod
    def create_specification(cls,  # pylint:disable=arguments-differ
                             build_config,
                             run_config,
                             to_dict=True):
        try:
            specification = BaseRunSpecification.create_specification(
                build_config=build_config, to_dict=True)
        except PolyaxonConfigurationError:
            raise PolyaxonConfigurationError(
                'Create specification expects a dict or an instance of BuildConfig.')

        if isinstance(run_config, RunConfig):
            r_config = run_config.to_light_dict()
        elif isinstance(run_config, Mapping):
            r_config = RunConfig.from_dict(run_config, unknown=EXCLUDE)
            r_config = r_config.to_light_dict()
        else:
            raise PolyaxonConfigurationError(
                'Create specification expects a dict or an instance of RunConfig.')

        specification[cls.KIND] = cls._SPEC_KIND
        specification[cls.RUN] = r_config

        if to_dict:
            return specification
        return cls.read(specification)
