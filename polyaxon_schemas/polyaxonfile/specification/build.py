# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy
from collections import Mapping

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile.specification.base import BaseSpecification
from polyaxon_schemas.polyaxonfile.utils import cached_property
from polyaxon_schemas.run_exec import BuildConfig, RunExecConfig


class BuildSpecification(BaseSpecification):
    """The polyaxonfile specification for build jobs.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        ENVIRONMENT: defines the run environment for experiment.
        BUILD: defines the build step where the user can set a docker image definition
    """
    _SPEC_KIND = BaseSpecification._BUILD

    def _extra_validation(self):
        if self.BUILD not in self.validated_data or not self.validated_data[self.BUILD]:
            raise PolyaxonConfigurationError(
                'Build specification must contain a valid `build` section.')

    @cached_property
    def parsed_data(self):
        return self._parsed_data

    @cached_property
    def validated_data(self):
        return self._validated_data

    @cached_property
    def build(self):
        return self.validated_data[self.BUILD]

    @cached_property
    def environment(self):
        return self.validated_data.get(self.ENVIRONMENT, None)

    @cached_property
    def resources(self):
        return self.environment.resources if self.environment else None

    @cached_property
    def node_selectors(self):
        return self.environment.node_selectors if self.environment else None

    @classmethod
    def create_specification(cls, build_config):
        if isinstance(build_config, BuildConfig):
            config = build_config.to_light_dict()
        elif isinstance(build_config, RunExecConfig):
            config = build_config.to_light_dict()
            config = BuildConfig.from_dict(config)
            config = config.to_light_dict()
        elif isinstance(build_config, Mapping):
            config = BuildConfig.from_dict(build_config)
            config = config.to_light_dict()
        else:
            raise PolyaxonConfigurationError(
                'Create specification expects a dict or an instance of BuildConfig.')

        return {
            cls.VERSION: 1,
            cls.KIND: cls._SPEC_KIND,
            cls.BUILD: config
        }
