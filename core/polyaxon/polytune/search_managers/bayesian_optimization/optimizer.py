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

from polyaxon.polytune.search_managers.bayesian_optimization.acquisition_function import (
    UtilityFunction,
)
from polyaxon.polytune.search_managers.bayesian_optimization.space import SearchSpace


class BOOptimizer:
    def __init__(self, config):
        self.space = SearchSpace(config=config)
        self.utility_function = UtilityFunction(
            config=config.utility_function, seed=config.seed
        )
        self.num_warmup = config.utility_function.num_warmup or 5
        self.num_iterations = config.utility_function.num_iterations or 10

    def _maximize(self):
        """ Find argmax of the acquisition function."""
        if not self.space.is_observations_valid():
            return None
        y_max = self.space.y.max()
        self.utility_function.gaussian_process.fit(self.space.x, self.space.y)
        return self.utility_function.max_compute(
            y_max=y_max,
            bounds=self.space.bounds,
            num_warmup=self.num_warmup,
            num_iterations=self.num_iterations,
        )

    def add_observations(self, configs, metrics):
        # Turn configs and metrics into data points
        self.space.add_observations(configs=configs, metrics=metrics)

    def get_suggestion(self):
        x = self._maximize()
        return self.space.get_suggestion(x)
