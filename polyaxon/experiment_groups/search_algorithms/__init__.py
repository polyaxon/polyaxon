from polyaxon_schemas.utils import SearchAlgorithms

from experiment_groups.search_algorithms import hyperband
from experiment_groups.search_algorithms import grid
from experiment_groups.search_algorithms import random


def get_suggestions(search_algorithm, matrix, n_suggestions, n_resumes):
    if SearchAlgorithms.is_grid(search_algorithm):
        return grid.get_suggestions(matrix=matrix, n_suggestions=n_suggestions, n_resumes=n_resumes)
    elif SearchAlgorithms.is_random(search_algorithm):
        return random.get_suggestions(matrix=matrix, n_suggestions=n_suggestions, n_resumes=n_resumes)

    return None

