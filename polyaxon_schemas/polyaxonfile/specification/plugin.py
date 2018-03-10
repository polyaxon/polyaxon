# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile.specification.base import BaseSpecification
from polyaxon_schemas.polyaxonfile.utils import cached_property


class PluginSpecification(BaseSpecification):
    """The polyaxonfile specification for plugins.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        PROJECT: defines the project name this specification belongs to (must be unique).
        ENVIRONMENT: defines the run environment for experiment.
        RUN_EXEC: defines the run step where the user can set a docker image to execute
    """

    def __init__(self, values):
        super(PluginSpecification, self).__init__(values=values)
        if (self.RUN_EXEC not in self.validated_data or
                not self.validated_data[self.RUN_EXEC] or
                self.validated_data[self.RUN_EXEC].cmd is not None):
            raise PolyaxonConfigurationError(
                'Plugin specification must contain a valid `run` section.')

    @classmethod
    def read(cls, values):
        if isinstance(values, cls):
            return values
        return cls(values=values)

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
