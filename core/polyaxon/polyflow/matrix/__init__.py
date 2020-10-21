#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Union

from polyaxon.polyflow.matrix.bayes import (
    AcquisitionFunctions,
    BayesSchema,
    GaussianProcessConfig,
    GaussianProcessesKernels,
    UtilityFunctionConfig,
    V1Bayes,
)
from polyaxon.polyflow.matrix.grid_search import GridSearchSchema, V1GridSearch
from polyaxon.polyflow.matrix.hyperband import HyperbandSchema, V1Hyperband
from polyaxon.polyflow.matrix.hyperopt import HyperoptSchema, V1Hyperopt
from polyaxon.polyflow.matrix.iterative import IterativeSchema, V1Iterative
from polyaxon.polyflow.matrix.kinds import V1MatrixKind
from polyaxon.polyflow.matrix.mapping import MappingSchema, V1Mapping
from polyaxon.polyflow.matrix.params import (
    HpChoiceSchema,
    HpGeomSpaceSchema,
    HpLinSpaceSchema,
    HpLogNormalSchema,
    HpLogSpaceSchema,
    HpLogUniformSchema,
    HpNormalSchema,
    HpParamSchema,
    HpPChoiceSchema,
    HpQLogNormalSchema,
    HpQLogUniformSchema,
    HpQNormalSchema,
    HpQUniformSchema,
    HpRangeSchema,
    HpUniformSchema,
    V1HpChoice,
    V1HpGeomSpace,
    V1HpLinSpace,
    V1HpLogNormal,
    V1HpLogSpace,
    V1HpLogUniform,
    V1HpNormal,
    V1HpParam,
    V1HpPChoice,
    V1HpQLogNormal,
    V1HpQLogUniform,
    V1HpQNormal,
    V1HpQUniform,
    V1HpRange,
    V1HpUniform,
)
from polyaxon.polyflow.matrix.random_search import RandomSearchSchema, V1RandomSearch
from polyaxon.schemas.base import BaseOneOfSchema


class MatrixSchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        V1MatrixKind.MAPPING: MappingSchema,
        V1MatrixKind.GRID: GridSearchSchema,
        V1MatrixKind.RANDOM: RandomSearchSchema,
        V1MatrixKind.HYPERBAND: HyperbandSchema,
        V1MatrixKind.BAYES: BayesSchema,
        V1MatrixKind.HYPEROPT: HyperoptSchema,
        V1MatrixKind.ITERATIVE: IterativeSchema,
    }


V1Matrix = Union[
    V1Mapping,
    V1GridSearch,
    V1RandomSearch,
    V1Hyperband,
    V1Bayes,
    V1Hyperopt,
    V1Iterative,
]


class MatrixMixin:
    def get_matrix_kind(self):
        raise NotImplementedError

    @property
    def has_mapping_matrix(self):
        return self.get_matrix_kind() == V1Mapping.IDENTIFIER

    @property
    def has_grid_search_matrix(self):
        return self.get_matrix_kind() == V1GridSearch.IDENTIFIER

    @property
    def has_random_search_matrix(self):
        return self.get_matrix_kind() == V1RandomSearch.IDENTIFIER

    @property
    def has_hyperband_matrix(self):
        return self.get_matrix_kind() == V1Hyperband.IDENTIFIER

    @property
    def has_bo_matrix(self):
        return self.get_matrix_kind() == V1Bayes.IDENTIFIER

    @property
    def has_hyperopt_matrix(self):
        return self.get_matrix_kind() == V1Hyperopt.IDENTIFIER

    @property
    def has_iterative_matrix(self):
        return self.get_matrix_kind() == V1Iterative.IDENTIFIER
