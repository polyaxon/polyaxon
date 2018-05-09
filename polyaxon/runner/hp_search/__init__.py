from polyaxon_schemas.utils import SearchAlgorithms
from runner.hp_search import bo, grid, hyperband, random


def create(experiment_group):
    if SearchAlgorithms.is_grid(experiment_group.search_algorithm):
        return grid.create(experiment_group=experiment_group)
    elif SearchAlgorithms.is_random(experiment_group.search_algorithm):
        return random.create(experiment_group=experiment_group)
    elif SearchAlgorithms.is_hyperband(experiment_group.search_algorithm):
        return hyperband.create(experiment_group=experiment_group)
    elif SearchAlgorithms.is_bo(experiment_group.search_algorithm):
        return bo.create(experiment_group=experiment_group)
    return None
