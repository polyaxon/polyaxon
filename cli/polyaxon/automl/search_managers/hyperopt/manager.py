import hyperopt

from polyaxon.automl.matrix.hyperopt import to_hyperopt
from polyaxon.automl.matrix.utils import to_numpy
from polyaxon.automl.search_managers.base import BaseManager
from polyaxon.automl.search_managers.utils import get_random_generator
from polyaxon.schemas.polyflow.workflows.automl.hyperopt import HyperoptConfig
from polyaxon.schemas.polyflow.workflows.matrix import (
    MatrixChoiceConfig,
    MatrixGeomSpaceConfig,
    MatrixLinSpaceConfig,
    MatrixLogSpaceConfig,
    MatrixRangeConfig,
)
from polyaxon.schemas.polyflow.workflows.metrics import Optimization


class HyperoptManager(BaseManager):
    """Hyperopt search strategy manager for hyperparameter optimization."""

    CONFIG = HyperoptConfig

    def __init__(self, config):
        super(HyperoptManager, self).__init__(config)
        self._param_to_value = {}
        self._search_space = {}
        self._set_search_space()

    def _set_search_space(self):
        for k, v in self.config.matrix.items():
            self._search_space[k] = to_hyperopt(k, v)

            if v.IDENTIFIER in {
                MatrixChoiceConfig.IDENTIFIER,
                MatrixRangeConfig.IDENTIFIER,
                MatrixLinSpaceConfig.IDENTIFIER,
                MatrixLogSpaceConfig.IDENTIFIER,
                MatrixGeomSpaceConfig.IDENTIFIER,
            }:
                # Get the categorical/discrete values mapping
                self._param_to_value[k] = to_numpy(v)

    def _get_previous_observations(self, hyperopt_domain, configs=None, metrics=None):
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
            if self.config.metric.optimization == Optimization.MAXIMIZE:
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

    def get_suggestions(self, configs=None, metrics=None):
        if not self.config.n_runs:
            raise ValueError("This search strategy requires `n_runs`.")
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
        new_ids = minimize.trials.new_trial_ids(self.config.n_runs)
        minimize.trials.refresh()
        random_state = minimize.rstate.randint(2 ** 31 - 1)
        new_trials = self.algorithm(
            new_ids, minimize.domain, hyperopt_trials, random_state
        )
        minimize.trials.refresh()

        for tid in range(self.config.n_runs):
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
