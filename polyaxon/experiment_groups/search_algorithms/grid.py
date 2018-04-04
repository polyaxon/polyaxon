import itertools


def get_suggestions(matrix, n_suggestions):
    """Return a list of suggestions based on grid search.

    Params:
        matrix: `dict` representing the {hyperparam: hyperparam matrix config}.
        n_suggestions: number of suggestions to make
    """

    suggestions = []
    keys = list(matrix.keys())
    values = [v.to_numpy() for v in matrix.values()]
    for v in itertools.product(*values):
        suggestions.append(dict(zip(keys, v)))

    if n_suggestions:
        return suggestions[:n_suggestions]
    return suggestions
