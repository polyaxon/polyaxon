from polyaxon.automl.search_managers.base import BaseManager
from polyaxon.automl.search_managers.bayesian_optimization.optimizer import BOOptimizer
from polyaxon.automl.search_managers.random_search.manager import RandomSearchManager
from polyaxon.schemas.polyflow.parallel import BOConfig, RandomSearchConfig


class BOSearchManager(BaseManager):
    """Bayesian optimization strategy manager for hyperparameter optimization."""

    CONFIG = BOConfig

    def __init__(self, config):
        super().__init__(config=config)
        self.n_initial_trials = self.config.n_initial_trials
        self.n_iterations = self.config.n_iterations

    def get_suggestions(self, configs=None, metrics=None):
        if not configs or not metrics:
            config = RandomSearchConfig(
                matrix=self.config.matrix,
                n_runs=self.n_initial_trials,
                seed=self.config.seed,
            )
            return RandomSearchManager(config=config).get_suggestions()

        optimizer = BOOptimizer(config=self.config)
        optimizer.add_observations(configs=configs, metrics=metrics)
        suggestion = optimizer.get_suggestion()
        return [suggestion] if suggestion else None

    def should_reschedule(self, iteration):
        """Return a boolean to indicate if we need to reschedule another iteration."""
        return iteration < self.n_iterations
