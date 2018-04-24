from experiment_groups.search_managers.base import BaseSearchAlgorithmManager
from experiment_groups.search_managers.bayesian_optimization.acquisition_function import (
    UtilityFunction
)
from polyaxon_schemas.utils import SearchAlgorithms

from experiment_groups.search_managers.bayesian_optimization.space import SearchSpace
from experiment_groups.search_managers.utils import get_random_suggestions


class BOManager(BaseSearchAlgorithmManager):
    """Bayesian optimization algorithm manager for hyperparameter optimization."""

    NAME = SearchAlgorithms.BO

    def __init__(self, params_config):
        super(BOManager, self).__init__(params_config=params_config)
        self.n_initial_trials = self.params_config.bo.n_initial_trials
        self.space = SearchSpace(params_config=params_config)
        self.utility_function = UtilityFunction(
            config=params_config.bo.utility_function, seed=params_config.seed)

    def _maximize(self):
        """ Find argmax of the acquisition function."""
        y_max = self.space.y.max()
        self.utility_function.gaussian_process.fit(self.space.x, self.space.y)
        return self.utility_function.max_compute(y_max=y_max, bounds=self.space.bounds)

    def _get_next_suggestion(self):
        x = self._maximize()
        return self.space.get_suggestion(x)

    def get_suggestions(self, iteration_config=None):
        if not iteration_config:
            return get_random_suggestions(matrix=self.params_config.matrix,
                                          n_suggestions=self.n_initial_trials,
                                          seed=self.params_config.seed)
        # Use the iteration_config to construct observed point and metrics
        experiments_configs = iteration_config.exepriments_configs
        experiments_metrics = iteration_config.exepriments_metrics
        # Turn configs and metrics into data points
        self.space.add_observations(configs=experiments_configs,
                                    metrics=experiments_metrics)

        return [self._get_next_suggestion()]
