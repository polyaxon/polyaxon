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
from typing import Dict, List

import hyperopt

from polyaxon.polyflow import (
    V1HpChoice,
    V1HpGeomSpace,
    V1HpLinSpace,
    V1HpLogSpace,
    V1HpRange,
    V1Hyperopt,
    V1Optimization,
)
from polyaxon.polytune.matrix.hyperopt import to_hyperopt
from polyaxon.polytune.matrix.utils import to_numpy
from polyaxon.polytune.search_managers.base import BaseManager
from polyaxon.polytune.search_managers.utils import get_random_generator


class HyperoptManager(BaseManager):
    """Hyperopt search strategy manager for hyperparameter optimization."""

    CONFIG = V1Hyperopt

    def __init__(self, config):
        super().__init__(config)
        self._param_to_value = {}
        self._search_space = {}
        self._set_search_space()
        self.max_iterations = self.config.max_iterations

    def _set_search_space(self):
        for k, v in self.config.params.items():
            self._search_space[k] = to_hyperopt(k, v)

            if v.IDENTIFIER in {
                V1HpChoice.IDENTIFIER,
                V1HpRange.IDENTIFIER,
                V1HpLinSpace.IDENTIFIER,
                V1HpLogSpace.IDENTIFIER,
                V1HpGeomSpace.IDENTIFIER,
            }:
                # Get the categorical/discrete values mapping
                self._param_to_value[k] = to_numpy(v)

    def _get_previous_observations(
        self, hyperopt_domain, configs: List[Dict] = None, metrics: List[float] = None
    ):
        # Previous observations
        trials = hyperopt.Trials()

        if not all([configs, metrics]):
            return trials

        observation_specs = []
        observation_results = []
        observation_miscs = []
        observation_ids = []

        for tid, observation_config in enumerate(configs):
            miscs_idxs = {}
            miscs_vals = {}
            observation_ids.append(tid)
            trial_misc = dict(
                tid=tid, cmd=hyperopt_domain.cmd, workdir=hyperopt_domain.workdir
            )

            for param in observation_config:

                observation_value = observation_config[param]
                if param in self._param_to_value:
                    index_of_value = self._param_to_value[param].index(
                        observation_value
                    )
                    miscs_idxs[param] = [tid]
                    miscs_vals[param] = [index_of_value]

                else:
                    miscs_idxs[param] = [tid]
                    miscs_vals[param] = [observation_value]

            observation_specs.append(None)

            trial_misc["idxs"] = miscs_idxs
            trial_misc["vals"] = miscs_vals
            observation_miscs.append(trial_misc)

            observation_metric = metrics[tid]
            if self.config.metric.optimization == V1Optimization.MAXIMIZE:
                observation_metric = -1 * observation_metric

            observation_results.append(
                {"loss": observation_metric, "status": hyperopt.STATUS_OK}
            )

        observations = trials.new_trial_docs(
            tids=observation_ids,
            specs=observation_specs,
            results=observation_results,
            miscs=observation_miscs,
        )

        for observation in observations:
            observation["state"] = hyperopt.JOB_STATE_DONE

        trials.insert_trial_docs(observations)
        trials.refresh()
        return trials

    @property
    def algorithm(self):
        if self.config.algorithm == "tpe":
            return hyperopt.tpe.suggest
        if self.config.algorithm == "rand":
            return hyperopt.rand.suggest
        if self.config.algorithm == "anneal":
            return hyperopt.anneal.suggest

    def get_suggestions(
        self, configs: List[Dict] = None, metrics: List[float] = None
    ) -> List[Dict]:
        if not self.config.num_runs:
            raise ValueError("This search strategy requires `num_runs`.")
        suggestions = []
        rand_generator = get_random_generator(seed=self.config.seed)
        hyperopt_domain = hyperopt.Domain(
            None, self._search_space, pass_expr_memo_ctrl=None
        )

        hyperopt_trials = self._get_previous_observations(
            hyperopt_domain=hyperopt_domain, configs=configs, metrics=metrics
        )

        minimize = hyperopt.FMinIter(
            self.config.algorithm,
            hyperopt_domain,
            hyperopt_trials,
            max_evals=-1,
            rstate=rand_generator,
            verbose=0,
        )

        minimize.catch_eval_exceptions = False
        new_ids = minimize.trials.new_trial_ids(self.config.num_runs)
        minimize.trials.refresh()
        random_state = minimize.rstate.randint(2 ** 31 - 1)
        new_trials = self.algorithm(
            new_ids, minimize.domain, hyperopt_trials, random_state
        )
        minimize.trials.refresh()

        for tid in range(self.config.num_runs):
            vals = new_trials[tid]["misc"]["vals"]
            suggestion = {}
            for param in vals:
                observation_value = vals[param][0]
                if param in self._param_to_value:
                    value = self._param_to_value[param][observation_value]
                    suggestion[param] = value
                else:
                    suggestion[param] = observation_value

            suggestions.append(suggestion)

        return suggestions
