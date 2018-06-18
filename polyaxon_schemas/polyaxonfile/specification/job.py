# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile.specification.base import BaseSpecification
from polyaxon_schemas.polyaxonfile.specification.build import BuildSpecification
from polyaxon_schemas.polyaxonfile.utils import cached_property
from polyaxon_schemas.run_exec import RunConfig


class JobSpecification(BuildSpecification):
    """The polyaxonfile specification for run jobs.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        LOGGING: defines the logging
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
        BUILD: defines the build step where the user can set a docker image definition
        RUN: defines the run step where the user can run a command
    """
    _SPEC_KIND = BaseSpecification._JOB  # pylint:disable=protected-access

    REQUIRED_SECTIONS = BuildSpecification.REQUIRED_SECTIONS + (
        BaseSpecification.RUN,
    )

    POSSIBLE_SECTIONS = BuildSpecification.POSSIBLE_SECTIONS + (
        BaseSpecification.RUN,
    )

    @cached_property
    def run(self):
        return self.validated_data.get(self.RUN, None)

    @classmethod
    def create_specification(cls,  # pylint:disable=arguments-differ
                             build_config,
                             run_config,
                             to_dict=True):
        try:
            specification = BuildSpecification.create_specification(
                build_config=build_config, to_dict=True)
        except PolyaxonConfigurationError:
            raise PolyaxonConfigurationError(
                'Create specification expects a dict or an instance of BuildConfig.')

        if isinstance(run_config, RunConfig):
            config = run_config.to_light_dict()
        elif isinstance(run_config, Mapping):
            config = RunConfig.from_dict(run_config)
            config = config.to_light_dict()
        else:
            raise PolyaxonConfigurationError(
                'Create specification expects a dict or an instance of RunConfig.')

        specification[cls.KIND] = cls._SPEC_KIND
        specification[cls.RUN] = config

        if to_dict:
            return specification
        return cls.read(specification)
