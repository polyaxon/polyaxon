from experiment_groups.search_managers.base import BaseSearchAlgorithmManager
from experiment_groups.search_managers.utils import get_random_suggestions
from polyaxon_schemas.utils import SearchAlgorithms


class RandomSearchManager(BaseSearchAlgorithmManager):
    """Random search algorithm manager for hyperparameter optimization."""

    NAME = SearchAlgorithms.RANDOM

    def get_suggestions(self, iteration_config=None):
        """Return a list of suggestions based on random search.

        Params:
            matrix: `dict` representing the {hyperparam: hyperparam matrix config}.
            n_suggestions: number of suggestions to make.
        """
        matrix = self.params_config.matrix
        n_suggestions = self.params_config.random_search.n_experiments
        seed = self.params_config.seed
        return get_random_suggestions(matrix=matrix, n_suggestions=n_suggestions, seed=seed)
