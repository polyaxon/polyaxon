from experiment_groups.search_algorithms.base import BaseSearchAlgorithm
from experiment_groups.search_algorithms.utils import Suggestion


class RandomSearch(BaseSearchAlgorithm):
    """Random search algorithm for hyperparameter optimization."""
    def get_suggestions(self):
        """Return a list of suggestions based on random search.

        Params:
            matrix: `dict` representing the {hyperparam: hyperparam matrix config}.
            n_suggestions: number of suggestions to make.
        """
        matrix = self.specification.matrix
        n_suggestions = self.specification.n_experiments

        if not n_suggestions:
            raise ValueError('This search algorithm requires `n_experiments`.')
        suggestions = []
        while n_suggestions > 0:
            params = {k: v.sample() for k, v in matrix.items()}
            suggestion = Suggestion(params=params)
            if suggestion not in suggestions:
                suggestions.append(suggestion)
                n_suggestions -= 1
        return [suggestion.params for suggestion in suggestions]
