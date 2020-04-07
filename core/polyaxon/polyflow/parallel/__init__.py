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

from polyaxon.polyflow.parallel.bayes import (
    AcquisitionFunctions,
    BayesSchema,
    GaussianProcessConfig,
    GaussianProcessesKernels,
    UtilityFunctionConfig,
    V1Bayes,
)
from polyaxon.polyflow.parallel.grid_search import GridSearchSchema, V1GridSearch
from polyaxon.polyflow.parallel.hyperband import HyperbandSchema, V1Hyperband
from polyaxon.polyflow.parallel.hyperopt import HyperoptSchema, V1Hyperopt
from polyaxon.polyflow.parallel.iterative import IterativeSchema, V1Iterative
from polyaxon.polyflow.parallel.mapping import MappingSchema, V1Mapping
from polyaxon.polyflow.parallel.random_search import RandomSearchSchema, V1RandomSearch
from polyaxon.schemas.base import BaseOneOfSchema


class ParallelSchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        V1Mapping.IDENTIFIER: MappingSchema,
        V1GridSearch.IDENTIFIER: GridSearchSchema,
        V1RandomSearch.IDENTIFIER: RandomSearchSchema,
        V1Hyperband.IDENTIFIER: HyperbandSchema,
        V1Bayes.IDENTIFIER: BayesSchema,
        V1Hyperopt.IDENTIFIER: HyperoptSchema,
        V1Iterative.IDENTIFIER: IterativeSchema,
    }


class ParallelMixin(object):
    def get_parallel_kind(self):
        raise NotImplementedError

    @property
    def has_mapping_parallel(self):
        return self.get_parallel_kind() == V1Mapping.IDENTIFIER

    @property
    def has_grid_search_parallel(self):
        return self.get_parallel_kind() == V1GridSearch.IDENTIFIER

    @property
    def has_random_search_parallel(self):
        return self.get_parallel_kind() == V1RandomSearch.IDENTIFIER

    @property
    def has_hyperband_parallel(self):
        return self.get_parallel_kind() == V1Hyperband.IDENTIFIER

    @property
    def has_bo_parallel(self):
        return self.get_parallel_kind() == V1Bayes.IDENTIFIER

    @property
    def has_hyperopt_parallel(self):
        return self.get_parallel_kind() == V1Hyperopt.IDENTIFIER

    @property
    def has_iterative_parallel(self):
        return self.get_parallel_kind() == V1Iterative.IDENTIFIER
