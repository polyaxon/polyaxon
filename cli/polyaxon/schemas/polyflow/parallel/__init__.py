#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

from polyaxon.schemas.polyflow.parallel.bo import BOConfig, BOSchema
from polyaxon.schemas.polyflow.parallel.grid_search import (
    GridSearchConfig,
    GridSearchSchema,
)
from polyaxon.schemas.polyflow.parallel.hyperband import (
    HyperbandConfig,
    HyperbandSchema,
)
from polyaxon.schemas.polyflow.parallel.hyperopt import HyperoptSchema, HyperoptConfig
from polyaxon.schemas.polyflow.parallel.random_search import (
    RandomSearchConfig,
    RandomSearchSchema,
)

from polyaxon.schemas.base import BaseOneOfSchema
from polyaxon.schemas.polyflow.parallel.iterative import (
    IterativeConfig,
    IterativeSchema,
)
from polyaxon.schemas.polyflow.parallel.mapping import MappingConfig, MappingSchema


class ParallelSchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        MappingConfig.IDENTIFIER: MappingSchema,
        GridSearchConfig.IDENTIFIER: GridSearchSchema,
        RandomSearchConfig.IDENTIFIER: RandomSearchSchema,
        HyperbandConfig.IDENTIFIER: HyperbandSchema,
        BOConfig.IDENTIFIER: BOSchema,
        HyperoptConfig.IDENTIFIER: HyperoptSchema,
        IterativeConfig.IDENTIFIER: IterativeSchema,
    }


class ParallelMixin(object):
    def get_parallel_kind(self):
        raise NotImplementedError()

    @property
    def has_mapping_parallel(self):
        return self.get_parallel_kind() == MappingConfig.IDENTIFIER

    @property
    def has_grid_search_parallel(self):
        return self.get_parallel_kind() == GridSearchConfig.IDENTIFIER

    @property
    def has_random_search_parallel(self):
        return self.get_parallel_kind() == RandomSearchConfig.IDENTIFIER

    @property
    def has_hyperband_parallel(self):
        return self.get_parallel_kind() == HyperbandConfig.IDENTIFIER

    @property
    def has_bo_parallel(self):
        return self.get_parallel_kind() == BOConfig.IDENTIFIER

    @property
    def has_hyperopt_parallel(self):
        return self.get_parallel_kind() == HyperoptConfig.IDENTIFIER

    @property
    def has_iterative_parallel(self):
        return self.get_parallel_kind() == IterativeConfig.IDENTIFIER
