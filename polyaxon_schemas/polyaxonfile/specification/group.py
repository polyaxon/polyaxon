# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from polyaxon_schemas.environments import PersistenceConfig
from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile import validator
from polyaxon_schemas.polyaxonfile.parser import Parser
from polyaxon_schemas.polyaxonfile.specification.base import BaseSpecification
from polyaxon_schemas.polyaxonfile.specification.experiment import ExperimentSpecification
from polyaxon_schemas.polyaxonfile.utils import cached_property
from polyaxon_schemas.utils import SearchAlgorithms


class GroupSpecification(BaseSpecification):
    """Parses Polyaxonfiles/Configuration, with matrix section definition.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        LOGGING: defines the logging
        TAGS: defines the tags
        HYPER_PARAMS: hyper params tuning and concurrent runs.
        ENVIRONMENT: defines the run environment for experiment.
        DECLARATIONS: variables/modules that can be reused.
        RUN: defines the run step where the user can set a docker image to execute
        MODEL: defines the model to use based on the declarative API.
        TRAIN: defines how to train a model and how to read the data.
        EVAL: defines how to evaluate a model and how to read the data.
    """

    _SPEC_KIND = BaseSpecification._GROUP

    HEADER_SECTIONS = ExperimentSpecification.HEADER_SECTIONS + (
        BaseSpecification.HP_TUNING,
    )
    REQUIRED_SECTIONS = ExperimentSpecification.REQUIRED_SECTIONS + (
        BaseSpecification.HP_TUNING,
    )
    POSSIBLE_SECTIONS = ExperimentSpecification.POSSIBLE_SECTIONS + (
        BaseSpecification.HP_TUNING,
    )

    def _extra_validation(self):
        if not self.matrix:
            raise PolyaxonConfigurationError(
                'A matrix definition is required for group specification.')

    def _set_parsed_data(self):
        # We need to validate that the data is correct
        # For that we just use a matrix declaration test
        parsed_data = Parser.parse(self, self._data, self.matrix_declaration_test)
        validator.validate(spec=self, data=parsed_data)

    def get_experiment_spec(self, matrix_declaration):
        """Returns and experiment spec for this group spec and the given matrix declaration."""
        parsed_data = Parser.parse(self, self._data, matrix_declaration)
        del parsed_data[self.HP_TUNING]
        validator.validate(spec=self, data=parsed_data)
        return ExperimentSpecification(values=[parsed_data, {'kind': self._EXPERIMENT}])

    @cached_property
    def environment(self):
        # This is a hack, in the future we need to gather the paths of the experiments
        parsed_data = Parser.parse(self, self._data, self.matrix_declaration_test)
        return parsed_data.get(self.ENVIRONMENT, None)

    @cached_property
    def persistence(self):
        persistence = self.environment.get('persistence') if self.environment else None
        return PersistenceConfig.from_dict(persistence) if persistence else None

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
