#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

import copy

from functools import reduce
from operator import mul
from typing import Dict, List

from polyaxon.polyflow import V1RandomSearch
from polyaxon.polytune.matrix.utils import get_length, sample
from polyaxon.polytune.search_managers.base import BaseManager
from polyaxon.polytune.search_managers.spec import SuggestionSpec
from polyaxon.polytune.search_managers.utils import get_random_generator


class RandomSearchManager(BaseManager):
    """Random search strategy manager for hyperparameter optimization."""

    CONFIG = V1RandomSearch

    def get_suggestions(self, params: Dict = None) -> List[Dict]:
        if not self.config.num_runs:
            raise ValueError("This search strategy requires `num_runs`.")
        suggestions = []
        params = params or {}
        rand_generator = get_random_generator(seed=self.config.seed)
        # Validate number of suggestions and total space
        all_discrete = True
        for v in self.config.params.values():
            if v.is_continuous:
                all_discrete = False
                break
        num_runs = self.config.num_runs
        if all_discrete:
            space = reduce(mul, [get_length(v) for v in self.config.params.values()])
            num_runs = self.config.num_runs if self.config.num_runs <= space else space

        while num_runs > 0:
            suggestion_params = copy.deepcopy(params)
            suggestion_params.update(
                {
                    k: sample(v, rand_generator=rand_generator)
                    for k, v in self.config.params.items()
                }
            )
            suggestion = SuggestionSpec(params=suggestion_params)
            if suggestion not in suggestions:
                suggestions.append(suggestion)
                num_runs -= 1
        return [suggestion.params for suggestion in suggestions]
