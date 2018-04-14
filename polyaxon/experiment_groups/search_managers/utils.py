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


def get_random_suggestions(matrix, n_suggestions):
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
