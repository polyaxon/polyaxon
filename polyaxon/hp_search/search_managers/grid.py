import itertools

from hp_search.search_managers.base import BaseSearchAlgorithmManager
from polyaxon_schemas.utils import SearchAlgorithms


class GridSearchManager(BaseSearchAlgorithmManager):
    """Grid search algorithm manager for hyperparameter optimization."""

    NAME = SearchAlgorithms.GRID

    def get_suggestions(self, iteration_config=None):
        """Return a list of suggestions based on grid search.

        Params:
            matrix: `dict` representing the {hyperparam: hyperparam matrix config}.
            n_suggestions: number of suggestions to make.
        """
        matrix = self.params_config.matrix

        suggestions = []
        keys = list(matrix.keys())
        values = [v.to_numpy() for v in matrix.values()]
        for v in itertools.product(*values):
            suggestions.append(dict(zip(keys, v)))

        if self.params_config.grid_search:
            n_suggestions = self.params_config.grid_search.n_experiments
            if n_suggestions:
                return suggestions[:n_suggestions]
        return suggestions
