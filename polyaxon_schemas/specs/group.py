# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from hestia.cached_property import cached_property

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.ops.group import GroupConfig
from polyaxon_schemas.ops.group.hptuning import SearchAlgorithms
from polyaxon_schemas.specs import kinds
from polyaxon_schemas.specs.base import BaseRunSpecification
from polyaxon_schemas.specs.experiment import ExperimentSpecification
from polyaxon_schemas.specs.libs import validator
from polyaxon_schemas.specs.libs.parser import Parser


class GroupSpecification(BaseRunSpecification):
    """Parses Polyaxonfiles/Configuration, with matrix section definition.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        LOGGING: defines the logging
        TAGS: defines the tags
        HYPER_PARAMS: hyper params tuning and concurrent runs.
        ENVIRONMENT: defines the run environment for experiment.
        PARAMS: variables/modules that can be reused.
        RUN: defines the run step where the user can set a docker image to execute
    """

    _SPEC_KIND = kinds.GROUP

    SECTIONS = ExperimentSpecification.SECTIONS + (
        BaseRunSpecification.HP_TUNING,
    )

    STD_PARSING_SECTIONS = ExperimentSpecification.STD_PARSING_SECTIONS + (
        BaseRunSpecification.HP_TUNING,
    )

    HEADER_SECTIONS = ExperimentSpecification.HEADER_SECTIONS + (
        BaseRunSpecification.HP_TUNING,
    )

    REQUIRED_SECTIONS = ExperimentSpecification.REQUIRED_SECTIONS + (
        BaseRunSpecification.HP_TUNING,
    )

    POSSIBLE_SECTIONS = ExperimentSpecification.POSSIBLE_SECTIONS + (
        BaseRunSpecification.HP_TUNING,
    )
    CONFIG = GroupConfig

    def _extra_validation(self):
        if not self.matrix:
            raise PolyaxonConfigurationError(
                'A matrix definition is required for group specification.')

    def parse_data(self, context=None):
        params = self._config_data.get_params(context=context)
        parsed_data = Parser.parse(self, self._config_data, params, self.matrix_declaration_test)
        validator.validate(spec=self, data=parsed_data)
        self._config = self._config_data
        return parsed_data

    def get_experiment_spec(self, matrix_declaration):
        """Returns an experiment spec for this group spec and the given matrix declaration."""
        params = self._config_data.get_params(context=matrix_declaration)
        parsed_data = Parser.parse(self, self._config_data, params, matrix_declaration)
        del parsed_data[self.HP_TUNING]
        return ExperimentSpecification(values=[parsed_data, {'kind': kinds.EXPERIMENT}])

    @cached_property
    def hptuning(self):
        return self.headers[self.HP_TUNING]

    @cached_property
    def matrix(self):
        if self.hptuning:
            return self.hptuning.matrix
        return None

    @cached_property
    def matrix_space(self):
        if not self.matrix:
            return 1

        space_size = 1

        for value in six.itervalues(self.matrix):
            space_size *= len(value.to_numpy())
        return space_size

    @cached_property
    def early_stopping(self):
        early_stopping = None
        if self.hptuning:
            early_stopping = self.hptuning.early_stopping
        return early_stopping or []

    @cached_property
    def search_algorithm(self):
        return self.hptuning.search_algorithm

    @cached_property
    def concurrency(self):
        concurrency = None
        if self.hptuning:
            concurrency = self.hptuning.concurrency
        return concurrency or 1

    @cached_property
    def experiments_def(self):
        definition = {
            'search_algorithm': self.search_algorithm,
            'early_stopping': True if self.early_stopping else False,
            'concurrency': self.concurrency
        }
        if SearchAlgorithms.is_grid(self.search_algorithm):
            if self.hptuning.grid_search and self.hptuning.grid_search.n_experiments:
                definition['n_experiments'] = self.hptuning.grid_search.n_experiments
        if SearchAlgorithms.is_random(self.search_algorithm):
            if self.hptuning.random_search and self.hptuning.random_search.n_experiments:
                definition['n_experiments'] = self.hptuning.random_search.n_experiments

        return definition

    @cached_property
    def matrix_declaration_test(self):
        if not self.matrix:
            return {}

        return {k: v.sample() for k, v in six.iteritems(self.matrix)}
