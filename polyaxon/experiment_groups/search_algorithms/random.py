import numpy as np

from experiment_groups.experiment_declaration import ExperimentDeclaration


def get_suggestions(matrix, n_experiments):
    """Return a list of suggestions based on random search.

    Params:
        matrix: `dict` representing the {hyperparam: hyperparam matrix config}.
        n_suggestions: number of suggestions to make
    """
    if not n_experiments:
        raise ValueError('This search algorithm requires `n_experiments`.')
    declarations = []
    declaration_matrix_params = {k: v.to_numpy() for k, v in matrix.items()}
    while n_experiments > 0:
        params = {k: np.random.choice(v) for k, v in declaration_matrix_params}
        declaration = ExperimentDeclaration(params=params)
        if declaration not in declarations:
            declarations.append(declaration)
            n_experiments -= 1
    return [declaration.params for declaration in declarations]
