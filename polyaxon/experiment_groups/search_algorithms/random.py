from experiment_groups.search_algorithms.base import BaseSearchAlgorithm
from experiment_groups.search_algorithms.utils import get_random_suggestions


class RandomSearch(BaseSearchAlgorithm):
    """Random search algorithm for hyperparameter optimization."""
    def get_suggestions(self, iteration=None):
        """Return a list of suggestions based on random search.

        Params:
            matrix: `dict` representing the {hyperparam: hyperparam matrix config}.
            n_suggestions: number of suggestions to make.
        """
        matrix = self.specification.matrix
        n_suggestions = self.specification.settings.random_search.n_experiments
        return get_random_suggestions(matrix=matrix, n_suggestions=n_suggestions)
