from polyaxon.automl.search_managers.bayesian_optimization.acquisition_function import (
    UtilityFunction,
)
from polyaxon.automl.search_managers.bayesian_optimization.space import SearchSpace


class BOOptimizer(object):
    def __init__(self, config):
        self.space = SearchSpace(config=config)
        self.utility_function = UtilityFunction(
            config=config.utility_function, seed=config.seed
        )
        self.n_warmup = config.utility_function.n_warmup or 5
        self.n_iter = config.utility_function.n_iter or 10

    def _maximize(self):
        """ Find argmax of the acquisition function."""
        if not self.space.is_observations_valid():
            return None
        y_max = self.space.y.max()
        self.utility_function.gaussian_process.fit(self.space.x, self.space.y)
        return self.utility_function.max_compute(
            y_max=y_max,
            bounds=self.space.bounds,
            n_warmup=self.n_warmup,
            n_iter=self.n_iter,
        )

    def add_observations(self, configs, metrics):
        # Turn configs and metrics into data points
        self.space.add_observations(configs=configs, metrics=metrics)

    def get_suggestion(self):
        x = self._maximize()
        return self.space.get_suggestion(x)
