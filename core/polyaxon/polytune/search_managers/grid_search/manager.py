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

import itertools

from typing import Dict, List

from polyaxon.polyflow import V1GridSearch
from polyaxon.polytune.matrix.utils import to_numpy
from polyaxon.polytune.search_managers.base import BaseManager


class GridSearchManager(BaseManager):
    """Grid search strategy manager for hyperparameter optimization."""

    CONFIG = V1GridSearch

    def get_suggestions(self, params: List[Dict] = None) -> List[Dict]:
        suggestions = []
        keys = list(self.config.params.keys())
        values = [to_numpy(v) for v in self.config.params.values()]
        for v in itertools.product(*values):
            suggestions.append(dict(zip(keys, v)))

        if self.config.num_runs:
            return suggestions[: self.config.num_runs]
        return suggestions
