from polyaxon_schemas.utils import SearchAlgorithms

from experiment_groups.search_managers.grid import GridSearchManager
from experiment_groups.search_managers.random import RandomSearchManager
from experiment_groups.search_managers.hyperband import HyperbandSearchManager


def get_search_algorithm_manager(specification):
    if SearchAlgorithms.is_grid(specification.search_algorithm):
        return GridSearchManager(specification=specification)
    elif SearchAlgorithms.is_random(specification.search_algorithm):
        return RandomSearchManager(specification=specification)
    elif SearchAlgorithms.is_hyperband(specification.search_algorithm):
        return HyperbandSearchManager(specification=specification)

    return None

