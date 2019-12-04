import copy

from functools import reduce
from operator import mul

from polyaxon.automl.matrix.utils import get_length, sample
from polyaxon.automl.search_managers.base import BaseManager
from polyaxon.automl.search_managers.spec import SuggestionSpec
from polyaxon.automl.search_managers.utils import get_random_generator
from polyaxon.schemas.polyflow.parallel import RandomSearchConfig


class RandomSearchManager(BaseManager):
    """Random search strategy manager for hyperparameter optimization."""

    CONFIG = RandomSearchConfig

    def get_suggestions(self, suggestion_params=None):
        if not self.config.n_runs:
            raise ValueError("This search strategy requires `n_runs`.")
        suggestions = []
        suggestion_params = suggestion_params or {}
        rand_generator = get_random_generator(seed=self.config.seed)
        # Validate number of suggestions and total space
        all_discrete = True
        for v in self.config.matrix.values():
            if v.is_continuous:
                all_discrete = False
                break
        n_runs = self.config.n_runs
        if all_discrete:
            space = reduce(mul, [get_length(v) for v in self.config.matrix.values()])
            n_runs = self.config.n_runs if self.config.n_runs <= space else space

        while n_runs > 0:
            params = copy.deepcopy(suggestion_params)
            params.update(
                {
                    k: sample(v, rand_generator=rand_generator)
                    for k, v in self.config.matrix.items()
                }
            )
            suggestion = SuggestionSpec(params=params)
            if suggestion not in suggestions:
                suggestions.append(suggestion)
                n_runs -= 1
        return [suggestion.params for suggestion in suggestions]
