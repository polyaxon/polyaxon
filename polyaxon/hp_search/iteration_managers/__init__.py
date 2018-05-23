from hp_search.iteration_managers import BOIterationManager
from hp_search.iteration_managers.hyperband import HyperbandIterationManager
from polyaxon_schemas.utils import SearchAlgorithms


def get_search_iteration_manager(experiment_group):
    if SearchAlgorithms.is_hyperband(experiment_group.search_algorithm):
        return HyperbandIterationManager(experiment_group=experiment_group)
    if SearchAlgorithms.is_bo(experiment_group.search_algorithm):
        return BOIterationManager(experiment_group=experiment_group)

    return None
