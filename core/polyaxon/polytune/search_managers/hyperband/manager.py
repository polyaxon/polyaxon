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

import math

from typing import Dict, List, Tuple

from polyaxon.polyflow import V1Hyperband, V1Optimization, V1RandomSearch
from polyaxon.polytune.search_managers.base import BaseManager
from polyaxon.polytune.search_managers.random_search.manager import RandomSearchManager


class HyperbandManager(BaseManager):
    """Hyperband search strategy manager for hyperparameter optimization.

    The strategy runs in the following way:

    def run(self):
        results = []

        for bracket in reversed(range(self.s_max)):
            num_runs = self.get_num_runs(bracket=bracket)
            num_resources = self.get_resources(bracket=bracket)

            suggestions = [get_suggestions(...) for _ in range(num_runs)]

            for bracket_iteration in range(bracket + 1):
                num_runs_to_keep = self.get_n_run_to_keep(
                    num_runs=num_runs, bracket_iteration=bracket_iteration)
                num_iterations = self.get_n_resources(
                    n_resources=n_resources, bracket_iteration=bracket_iteration)

                val_losses = []
                early_stops = []

                for suggestion in suggestions:
                    result = run_suggestions(num_iterations, suggestion)
                    loss = result['loss']
                    val_losses.append(loss)
                    early_stop = result.get('early_stop', False)
                    early_stops.append(early_stop)
                    results.append(result)

                # select a number of best configurations for the next loop
                # filter out early stops, if any
                indices = np.argsort(val_losses)
                suggestions = [suggestions[i] for i in indices if not early_stops[i]]
                suggestions = suggestions[:num_runs_to_keep]

        return results
    """

    CONFIG = V1Hyperband

    def __init__(self, config):
        super().__init__(config)
        self.config.set_tuning_params()

    def get_resources(self, bracket):
        # r: initial number of iterations/resources per config
        return self.config.max_iterations * (self.config.eta ** (-bracket))

    def get_resources_for_iteration(self, iteration):
        bracket = self.config.get_bracket(iteration=iteration)
        return self.get_resources(bracket=bracket)

    def get_n_resources(self, n_resources, bracket_iteration):
        """Return the number of iterations to run for this barcket_i"""
        return n_resources * self.config.eta ** bracket_iteration

    def get_n_resources_for_iteration(self, iteration, bracket_iteration):
        """Return the number of iterations to run for this barcket_i

        This is just util function around `get_n_resources`
        """
        n_resources = self.get_resources_for_iteration(iteration=iteration)
        return self.get_n_resources(
            n_resources=n_resources, bracket_iteration=bracket_iteration
        )

    def get_suggestions(
        self,
        iteration: int,
        bracket_iteration: int,
        configs: List[Dict] = None,
        metrics: List[float] = None,
    ) -> List[Dict]:
        """Return a list of suggestions/arms based on hyperband."""
        if configs:
            return self.get_bracket_suggestions(
                bracket_iteration=bracket_iteration, configs=configs, metrics=metrics
            )
        else:
            return self.get_iteration_suggestions(
                iteration=iteration, bracket_iteration=bracket_iteration
            )

    def get_iteration_suggestions(self, iteration: int, bracket_iteration: int):
        """Return a list of suggestions for initial iteration."""
        bracket = self.config.get_bracket(iteration=iteration)
        num_runs = self.config.get_num_runs(bracket=bracket)
        n_resources = self.get_n_resources_for_iteration(
            iteration=iteration, bracket_iteration=bracket_iteration
        )
        n_resources = self.config.resource.cast_value(n_resources)
        suggestion_params = {self.config.resource.name: n_resources}
        config = V1RandomSearch(
            params=self.config.params, num_runs=num_runs, seed=self.config.seed
        )
        return RandomSearchManager(config=config).get_suggestions(
            params=suggestion_params
        )

    def get_bracket_suggestions(
        self, bracket_iteration: int, configs=None, metrics=None
    ):
        """Reduce the experiments to restart."""
        # Get the number of experiments to keep
        n_configs_to_keep = self.config.get_num_runs_to_keep(
            num_runs=len(configs),
            bracket_iteration=bracket_iteration,
        )

        # Order the experiments
        experiments = zip(configs, metrics)
        experiments = sorted(
            experiments,
            key=lambda x: x[1],
            reverse=V1Optimization.maximize(self.config.metric.optimization),
        )
        # Keep n experiments config
        return [xp[0] for xp in experiments[:n_configs_to_keep]]
