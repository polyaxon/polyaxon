# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import itertools
import six

from marshmallow import ValidationError

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile import validator
from polyaxon_schemas.polyaxonfile import reader
from polyaxon_schemas.polyaxonfile.parser import Parser
from polyaxon_schemas.polyaxonfile.specification.experiment import Specification
from polyaxon_schemas.polyaxonfile.specification.base import BaseSpecification
from polyaxon_schemas.polyaxonfile.utils import cached_property
from polyaxon_schemas.utils import to_list, SEARCH_METHODS


class GroupSpecification(BaseSpecification):
    """Parses Polyaxonfiles/Configuration, with matrix section definition.

    SECTIONS:
        VERSION: defines the version of the file to be parsed and validated.
        PROJECT: defines the project name this specification belongs to (must be unique).
        SETTINGS: defines the logging, run type and concurrent runs.
        ENVIRONMENT: defines the run environment for experiment.
        MATRIX: hyper parameters matrix definition.
        DECLARATIONS: variables/modules that can be reused.
        RUN_EXEC: defines the run step where the user can set a docker image to execute
        MODEL: defines the model to use based on the declarative API.
        TRAIN: defines how to train a model and how to read the data.
        EVAL: defines how to evaluate a model and how to read the data.
    """

    def __init__(self, values):
        self._values = to_list(values)

        self._data = reader.read(self._values)
        Parser.check_data(spec=self, data=self._data)
        headers = Parser.get_headers(spec=self, data=self._data)
        matrix = Parser.get_matrix(spec=self, data=self._data)
        try:
            self._matrix = validator.validate_matrix(matrix)
        except ValidationError as e:
            raise PolyaxonConfigurationError(e)
        try:
            self._headers = validator.validate_headers(spec=self, data=headers)
        except ValidationError as e:
            raise PolyaxonConfigurationError(e)
        self._parsed_data = []
        self._validated_data = []
        self._experiment_specs = []

        matrix_declarations = self.matrix_declarations if self.matrix_declarations else [{}]
        for i, matrix_declaration in enumerate(matrix_declarations):
            parsed_data = Parser.parse(self, self._data, matrix_declaration)
            self._validated_data.append(validator.validate(spec=self, data=parsed_data))
            self._parsed_data.append(parsed_data)
            self._experiment_specs.append(Specification(experiment=i, values=parsed_data))

    @cached_property
    def experiment_specs(self):
        return self._experiment_specs

    @cached_property
    def matrix(self):
        return self._matrix

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
        if self.settings:
            early_stopping = self.settings.early_stopping
        return early_stopping or []

    @cached_property
    def n_experiments(self):
        if not self.settings or not self.settings.n_experiments or not self.matrix_space:
            return None

        n_experiments = self.settings.n_experiments
        # Check the if the n_experiments is percent
        if n_experiments < 1:
            return int(self.matrix_space * n_experiments)

        return int(n_experiments) if n_experiments < self.matrix_space else None

    @cached_property
    def search_method(self):
        search_method = None
        if self.settings:
            search_method = self.settings.search_method
        return search_method or SEARCH_METHODS.SEQUENTIAL

    @cached_property
    def concurrent_experiments(self):
        concurrent_experiments = None
        if self.settings:
            concurrent_experiments = self.settings.concurrent_experiments
        return concurrent_experiments or 1

    @cached_property
    def experiments_def(self):
        return (
            self.matrix_space,
            self.n_experiments,
            self.concurrent_experiments,
            self.search_method
        )

    @cached_property
    def matrix_declarations(self):
        if not self.matrix:
            return []

        declarations = []
        keys = list(six.iterkeys(self.matrix))
        values = [v.to_numpy() for v in six.itervalues(self.matrix)]
        for v in itertools.product(*values):
            declarations.append(dict(zip(keys, v)))

        if len(declarations) != self.matrix_space:
            raise PolyaxonConfigurationError('The matrix declaration is not valid.')
        return declarations

    def get_declarations_at(self, experiment):
        if experiment > self.matrix_space:
            raise ValueError("""Could not find an experiment at index {},
               this file has {} experiments""".format(experiment, self.matrix_space))
        return self.matrix_declarations[experiment]

    def experiment_spec_at(self, experiment):
        if experiment > self.matrix_space:
            raise ValueError("""Could not find an experiment at index {},
               this file has {} experiments""".format(experiment, self.matrix_space))
        return self.experiment_specs[experiment]

