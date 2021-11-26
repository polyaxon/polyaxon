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
from typing import Dict, List

from polyaxon.polyflow import V1Bayes, V1RandomSearch
from polyaxon.polytune.search_managers.base import BaseManager
from polyaxon.polytune.search_managers.bayesian_optimization.optimizer import (
    BOOptimizer,
)
from polyaxon.polytune.search_managers.random_search.manager import RandomSearchManager


class BayesSearchManager(BaseManager):
    """Bayesian optimization strategy manager for hyperparameter optimization."""

    CONFIG = V1Bayes

    def __init__(self, config):
        super().__init__(config=config)
        self.num_initial_runs = self.config.num_initial_runs
        self.max_iterations = self.config.max_iterations

    def get_suggestions(
        self, configs: List[Dict] = None, metrics: List[float] = None
    ) -> List[Dict]:
        if not configs or not metrics:
            config = V1RandomSearch(
                params=self.config.params,
                num_runs=self.num_initial_runs,
                seed=self.config.seed,
            )
            return RandomSearchManager(config=config).get_suggestions()

        optimizer = BOOptimizer(config=self.config)
        optimizer.add_observations(configs=configs, metrics=metrics)
        suggestion = optimizer.get_suggestion()
        return [suggestion] if suggestion else None
