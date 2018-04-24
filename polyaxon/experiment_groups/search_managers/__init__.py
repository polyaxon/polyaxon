from polyaxon_schemas.utils import SearchAlgorithms

from experiment_groups.search_managers.bayesian_optimization.manager import BOSearchManager
from experiment_groups.search_managers.grid import GridSearchManager
from experiment_groups.search_managers.random import RandomSearchManager
from experiment_groups.search_managers.hyperband import HyperbandSearchManager


def get_search_algorithm_manager(params_config):
    if not params_config:
        return None

    if SearchAlgorithms.is_grid(params_config.search_algorithm):
        return GridSearchManager(params_config=params_config)
    if SearchAlgorithms.is_random(params_config.search_algorithm):
        return RandomSearchManager(params_config=params_config)
    if SearchAlgorithms.is_hyperband(params_config.search_algorithm):
        return HyperbandSearchManager(params_config=params_config)
    if SearchAlgorithms.is_bo(params_config.search_algorithm):
        return BOSearchManager(params_config=params_config)

    return None

