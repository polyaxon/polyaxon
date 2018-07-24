# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

from polyaxon_schemas.build import BuildConfig
from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile.specification.base import BaseSpecification
from polyaxon_schemas.polyaxonfile.utils import cached_property


class BuildSpecification(BaseSpecification):
    """The polyaxonfile specification for build jobs.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        LOGGING: defines the logging
        TAGS: defines the tags
        ENVIRONMENT: defines the run environment for experiment.
        BUILD: defines the build step where the user can set a docker image definition
    """
    _SPEC_KIND = BaseSpecification._BUILD

    REQUIRED_SECTIONS = BaseSpecification.REQUIRED_SECTIONS + (
        BaseSpecification.BUILD,
    )
    POSSIBLE_SECTIONS = BaseSpecification.POSSIBLE_SECTIONS + (
        BaseSpecification.ENVIRONMENT, BaseSpecification.BUILD,
    )

    @cached_property
    def validated_data(self):
        return self._validated_data

    @cached_property
    def build(self):
        return self.validated_data.get(self.BUILD, None)

    @cached_property
    def environment(self):
        return self.validated_data.get(self.ENVIRONMENT, None)

    @cached_property
    def resources(self):
        return self.environment.resources if self.environment else None

    @cached_property
    def persistence(self):
        return self.environment.persistence if self.environment else None

    @cached_property
    def outputs(self):
        return self.environment.outputs if self.environment else None

    @cached_property
    def node_selector(self):
        return self.environment.node_selector if self.environment else None

    @cached_property
    def affinity(self):
        return self.environment.affinity if self.environment else None

    @cached_property
    def tolerations(self):
        return self.environment.tolerations if self.environment else None

    @classmethod
    def create_specification(cls, build_config, to_dict=True):
        if isinstance(build_config, BuildConfig):
            config = build_config.to_light_dict()
        elif isinstance(build_config, Mapping):
            config = BuildConfig.from_dict(build_config)
            config = config.to_light_dict()
        else:
            raise PolyaxonConfigurationError(
                'Create specification expects a dict or an instance of BuildConfig.')

        specification = {
            cls.VERSION: 1,
            cls.KIND: cls._SPEC_KIND,
            cls.BUILD: config
        }

        if to_dict:
            return specification
        return cls.read(specification)
