from experiment_groups.search_managers.bayesian_optimization.acquisition_function import (
    UtilityFunction
)
from experiment_groups.search_managers.bayesian_optimization.space import SearchSpace


class BOOptimizer(object):
    def __init__(self, params_config):
        self.params_config = params_config
        self.n_initial_trials = self.params_config.bo.n_initial_trials
        self.space = SearchSpace(params_config=params_config)
        self.utility_function = UtilityFunction(
            config=params_config.bo.utility_function, seed=params_config.seed)

    def _maximize(self):
        """ Find argmax of the acquisition function."""
        if not self.space.is_observations_valid():
            return None
        y_max = self.space.y.max()
        self.utility_function.gaussian_process.fit(self.space.x, self.space.y)
        return self.utility_function.max_compute(y_max=y_max, bounds=self.space.bounds)

    def add_observations(self, configs, metrics):
        # Turn configs and metrics into data points
        self.space.add_observations(configs=configs, metrics=metrics)

    def get_suggestion(self):
        x = self._maximize()
        return self.space.get_suggestion(x)
