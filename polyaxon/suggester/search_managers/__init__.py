from suggester.search_managers.bayesian_optimization.manager import BOSearchManager
from suggester.search_managers.grid import GridSearchManager
from suggester.search_managers import HyperbandSearchManager
from suggester.search_managers import RandomSearchManager
from polyaxon_schemas.utils import SearchAlgorithms


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
