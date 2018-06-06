from hpsearch.search_managers.bayesian_optimization.manager import BOSearchManager
from hpsearch.search_managers.grid import GridSearchManager
from hpsearch.search_managers.hyperband import HyperbandSearchManager
from hpsearch.search_managers.random import RandomSearchManager
from polyaxon_schemas.utils import SearchAlgorithms


def get_search_algorithm_manager(hptuning_config):
    if not hptuning_config:
        return None

    if SearchAlgorithms.is_grid(hptuning_config.search_algorithm):
        return GridSearchManager(hptuning_config=hptuning_config)
    if SearchAlgorithms.is_random(hptuning_config.search_algorithm):
        return RandomSearchManager(hptuning_config=hptuning_config)
    if SearchAlgorithms.is_hyperband(hptuning_config.search_algorithm):
        return HyperbandSearchManager(hptuning_config=hptuning_config)
    if SearchAlgorithms.is_bo(hptuning_config.search_algorithm):
        return BOSearchManager(hptuning_config=hptuning_config)

    return None
