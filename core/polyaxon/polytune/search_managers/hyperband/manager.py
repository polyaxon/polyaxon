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
        # Maximum iterations per configuration
        self.max_iterations = config.max_iterations
        # Defines configuration downsampling/elimination rate (default = 3)
        self.eta = config.eta
        # number of times to run hyperband (brackets)
        self.s_max = int(math.log(self.max_iterations) / math.log(self.eta))
        # i.e.  # of times to repeat the outer loops over the tradeoffs `s`
        self.B = (
            self.s_max + 1
        ) * self.max_iterations  # budget per bracket of successive halving

    def get_bracket(self, iteration):
        """This defines the bracket `s` in outerloop `for s in reversed(range(self.s_max))`."""
        return self.s_max - iteration

    def get_num_runs(self, bracket):
        # n: initial number of configs
        return int(
            math.ceil(
                (self.B / self.max_iterations) * (self.eta ** bracket) / (bracket + 1)
            )
        )

    def get_resources(self, bracket):
        # r: initial number of iterations/resources per config
        return self.max_iterations * (self.eta ** (-bracket))

    def get_resources_for_iteration(self, iteration):
        bracket = self.get_bracket(iteration=iteration)
        return self.get_resources(bracket=bracket)

    def get_num_runs_to_keep(self, num_runs, bracket_iteration):
        """Return the number of configs to keep and resume."""
        num_runs = num_runs * (self.eta ** -bracket_iteration)
        return int(num_runs / self.eta)

    def get_num_runs_to_keep_for_iteration(self, iteration, bracket_iteration):
        """Return the number of configs to keep for an iteration and iteration bracket.

        This is just util function around `get_num_runs_to_keep`
        """
        bracket = self.get_bracket(iteration=iteration)
        if bracket_iteration == bracket + 1:
            # End of loop `for bracket_iteration in range(bracket + 1):`
            return 0

        num_runs = self.get_num_runs(bracket=bracket)
        return self.get_num_runs_to_keep(
            num_runs=num_runs, bracket_iteration=bracket_iteration
        )

    def get_n_resources(self, n_resources, bracket_iteration):
        """Return the number of iterations to run for this barcket_i"""
        return n_resources * self.eta ** bracket_iteration

    def get_n_resources_for_iteration(self, iteration, bracket_iteration):
        """Return the number of iterations to run for this barcket_i

        This is just util function around `get_n_resources`
        """
        n_resources = self.get_resources_for_iteration(iteration=iteration)
        return self.get_n_resources(
            n_resources=n_resources, bracket_iteration=bracket_iteration
        )

    def should_reschedule(self, iteration, bracket_iteration):
        """Return a boolean to indicate if we need to reschedule another iteration."""
        bracket = self.get_bracket(iteration=iteration)
        if bracket_iteration < bracket:
            # The bracket is still processing
            return False

        # We can only reschedule if we can create a new bracket
        return self.get_bracket(iteration=iteration + 1) >= 0

    def should_reduce_configs(self, iteration, bracket_iteration):
        """Return a boolean to indicate if we need to reschedule another bracket iteration."""
        num_runs_to_keep = self.get_num_runs_to_keep_for_iteration(
            iteration=iteration, bracket_iteration=bracket_iteration
        )
        return num_runs_to_keep > 0

    def create_iteration(
        self, iteration: int = 0, bracket_iteration: int = 0
    ) -> Tuple[int, int]:
        """Create an iteration for hyperband."""

        should_reschedule = self.should_reschedule(
            iteration=iteration, bracket_iteration=bracket_iteration,
        )
        should_reduce_configs = self.should_reduce_configs(
            iteration=iteration, bracket_iteration=bracket_iteration,
        )
        if should_reschedule:
            iteration = iteration + 1
            bracket_iteration = 0
        elif should_reduce_configs:
            bracket_iteration = bracket_iteration + 1
        else:
            raise ValueError(
                "Hyperband create iteration failed, "
                "could not reschedule ot reduce configs"
            )

        return iteration, bracket_iteration

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
        bracket = self.get_bracket(iteration=iteration)
        num_runs = self.get_num_runs(bracket=bracket)
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
        n_configs_to_keep = self.get_num_runs_to_keep(
            num_runs=len(configs), bracket_iteration=bracket_iteration,
        )

        # Order the experiments
        experiments = zip(configs, metrics)
        experiments = sorted(
            experiments,
            key=lambda x: x[1],
            reverse=V1Optimization.maximize(self.config.optimization),
        )
        # Keep n experiments config
        return [xp[0] for xp in experiments[:n_configs_to_keep]]
