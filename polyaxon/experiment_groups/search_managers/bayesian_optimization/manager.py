from experiment_groups.search_managers.base import BaseSearchAlgorithmManager
from experiment_groups.search_managers.bayesian_optimization.optimizer import BOOptimizer
from experiment_groups.search_managers.utils import get_random_suggestions
from polyaxon_schemas.utils import SearchAlgorithms


class BOSearchManager(BaseSearchAlgorithmManager):
    """Bayesian optimization algorithm manager for hyperparameter optimization."""

    NAME = SearchAlgorithms.BO

    def __init__(self, params_config):
        super(BOSearchManager, self).__init__(params_config=params_config)
        self.n_initial_trials = self.params_config.bo.n_initial_trials
        self.n_iterations = self.params_config.bo.n_iterations

    def get_suggestions(self, iteration_config=None):
        if not iteration_config:
            return get_random_suggestions(matrix=self.params_config.matrix,
                                          n_suggestions=self.n_initial_trials,
                                          seed=self.params_config.seed)
        # Use the iteration_config to construct observed point and metrics
        experiments_configs = dict(iteration_config.combined_experiments_configs)
        experiments_metrics = dict(iteration_config.combined_experiments_metrics)
        configs = []
        metrics = []
        for key in experiments_metrics.keys():
            configs.append(experiments_configs[key])
            metrics.append(experiments_metrics[key])
        optimizer = BOOptimizer(params_config=self.params_config)
        optimizer.add_observations(configs=configs, metrics=metrics)
        return [optimizer.get_suggestion()]

    def should_reschedule(self, iteration):
        """Return a boolean to indicate if we need to reschedule another iteration."""
        return iteration < self.n_iterations
