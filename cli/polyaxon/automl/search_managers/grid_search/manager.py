import itertools

from polyaxon.automl.matrix.utils import to_numpy
from polyaxon.automl.search_managers.base import BaseManager
from polyaxon.schemas.polyflow.parallel import GridSearchConfig


class GridSearchManager(BaseManager):
    """Grid search strategy manager for hyperparameter optimization."""

    CONFIG = GridSearchConfig

    def get_suggestions(self):
        suggestions = []
        keys = list(self.config.matrix.keys())
        values = [to_numpy(v) for v in self.config.matrix.values()]
        for v in itertools.product(*values):
            suggestions.append(dict(zip(keys, v)))

        if self.config.n_runs:
            return suggestions[: self.config.n_runs]
        return suggestions
