import itertools

from experiment_groups.search_algorithms.base import BaseSearchAlgorithm


class GridSearch(BaseSearchAlgorithm):
    """Grid search algorithm for hyperparameter optimization."""
    def get_suggestions(self, iteration=None):
        """Return a list of suggestions based on grid search.

        Params:
            matrix: `dict` representing the {hyperparam: hyperparam matrix config}.
            n_suggestions: number of suggestions to make.
        """
        matrix = self.specification.matrix
        n_suggestions = self.specification.matrix_space

        suggestions = []
        keys = list(matrix.keys())
        values = [v.to_numpy() for v in matrix.values()]
        for v in itertools.product(*values):
            suggestions.append(dict(zip(keys, v)))

        if n_suggestions:
            return suggestions[:n_suggestions]
        return suggestions
