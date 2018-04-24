import copy
import numpy as np
import uuid


class Suggestion(object):
    """A structure that defines an experiment hyperparam suggestion."""

    def __init__(self, params):
        self.params = params

    def __eq__(self, other):
        if self.params.keys() != other.params.keys():
            return False

        for key, value in self.params.items():
            if value != other.params[key]:
                return False

        return True

    def __repr__(self):
        return ','.join([
            '{}:{}'.format(key, val)
            for (key, val) in sorted(self.params.items())])

    def __hash__(self):
        return hash(self.__repr__())

    def uuid(self):
        return uuid.uuid5(uuid.NAMESPACE_DNS, self.__repr__())


def get_random_generator(seed=None):
    return np.random.RandomState(seed) if seed else np.random


def get_random_suggestions(matrix, n_suggestions, suggestion_params=None, seed=None):
    if not n_suggestions:
        raise ValueError('This search algorithm requires `n_experiments`.')
    suggestions = []
    suggestion_params = suggestion_params or {}
    rand_generator = get_random_generator(seed=seed)
    while n_suggestions > 0:
        params = copy.deepcopy(suggestion_params)
        params.update({k: v.sample(rand_generator=rand_generator) for k, v in matrix.items()})
        suggestion = Suggestion(params=params)
        if suggestion not in suggestions:
            suggestions.append(suggestion)
            n_suggestions -= 1
    return [suggestion.params for suggestion in suggestions]
