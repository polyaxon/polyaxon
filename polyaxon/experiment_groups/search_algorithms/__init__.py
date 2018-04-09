from experiment_groups.search_algorithms import grid, hyperband, random
from polyaxon_schemas.utils import SearchAlgorithms

from experiment_groups.search_algorithms.grid import GridSearch
from experiment_groups.search_algorithms.random import RandomSearch


def get_search_algorithm(specification):
    if SearchAlgorithms.is_grid(specification.search_algorithm):
        return GridSearch(specification=specification)
    elif SearchAlgorithms.is_random(specification.search_algorithm):
        return RandomSearch(specification=specification)

    return None
