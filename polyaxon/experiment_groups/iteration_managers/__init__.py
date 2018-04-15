from polyaxon_schemas.utils import SearchAlgorithms

from experiment_groups.iteration_managers.hyperband import HyperbandIterationManager


def get_search_iteration_manager(experiment_group):
    if SearchAlgorithms.is_hyperband(experiment_group.search_algorithm):
        return HyperbandIterationManager(experiment_group=experiment_group)

    return None
