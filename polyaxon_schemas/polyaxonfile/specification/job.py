# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import Mapping

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile.specification.base import BaseSpecification
from polyaxon_schemas.polyaxonfile.utils import cached_property
from polyaxon_schemas.run_exec import RunExecConfig


class JobSpecification(BaseSpecification):
    """The polyaxonfile specification for run jobs.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        ENVIRONMENT: defines the run environment for experiment.
        RUN_EXEC: defines the build step where the user can set a docker image definition
    """
    _SPEC_KIND = BaseSpecification._JOB

    def _extra_validation(self):
        if self.RUN_EXEC not in self.validated_data or not self.validated_data[self.RUN_EXEC]:
            raise PolyaxonConfigurationError(
                'Job specification must contain a valid `run` section.')

    @cached_property
    def parsed_data(self):
        return self._parsed_data

    @cached_property
    def validated_data(self):
        return self._validated_data

    @cached_property
    def run_exec(self):
        return self.validated_data[self.RUN_EXEC]

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
    def create_specification(cls, run_config, to_dict=True):
        if isinstance(run_config, RunExecConfig):
            config = run_config.to_light_dict()
        elif isinstance(run_config, Mapping):
            config = RunExecConfig.from_dict(run_config)
            config = config.to_light_dict()
        else:
            raise PolyaxonConfigurationError(
                'Create specification expects a dict or an instance of RunExecConfig.')

        specification = {
            cls.VERSION: 1,
            cls.KIND: cls._SPEC_KIND,
            cls.RUN_EXEC: config
        }

        if to_dict:
            return specification
        return cls.read(specification)
