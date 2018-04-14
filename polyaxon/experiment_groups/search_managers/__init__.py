from polyaxon_schemas.utils import SearchAlgorithms

from experiment_groups.search_managers.grid import GridSearchManager
from experiment_groups.search_managers.random import RandomSearchManager
from experiment_groups.search_managers.hyperband import HyperBandSearchManager
from experiment_groups.search_managers.schemas import HyperbandIterationConfig


def get_search_algorithm_manager(specification):
    if SearchAlgorithms.is_grid(specification.search_algorithm):
        return GridSearchManager(specification=specification)
    elif SearchAlgorithms.is_random(specification.search_algorithm):
        return RandomSearchManager(specification=specification)
    elif SearchAlgorithms.is_hyperband(specification.search_algorithm):
        return HyperBandSearchManager(specification=specification)

    return None


def get_iteration_config(search_algorithm, iteration=None):
    if SearchAlgorithms.is_grid(search_algorithm):
        return None
    elif SearchAlgorithms.is_random(search_algorithm):
        return None
    elif SearchAlgorithms.is_hyperband(search_algorithm):
        if not iteration:
            raise ValueError('No iteration was provided')
        return HyperbandIterationConfig.from_dict(iteration)

    return None

