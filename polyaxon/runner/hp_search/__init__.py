from polyaxon_schemas.utils import SearchAlgorithms

import auditor
from event_manager.events.experiment_group import EXPERIMENT_GROUP_GRID, EXPERIMENT_GROUP_RANDOM, \
    EXPERIMENT_GROUP_HYPERBAND, EXPERIMENT_GROUP_BO
from runner.hp_search import bo, grid, hyperband, random


def create(experiment_group):
    if SearchAlgorithms.is_grid(experiment_group.search_algorithm):
        auditor.record(event_type=EXPERIMENT_GROUP_GRID,
                       instance=experiment_group)
        return grid.create(experiment_group=experiment_group)
    elif SearchAlgorithms.is_random(experiment_group.search_algorithm):
        auditor.record(event_type=EXPERIMENT_GROUP_RANDOM,
                       instance=experiment_group)
        return random.create(experiment_group=experiment_group)
    elif SearchAlgorithms.is_hyperband(experiment_group.search_algorithm):
        auditor.record(event_type=EXPERIMENT_GROUP_HYPERBAND,
                       instance=experiment_group)
        return hyperband.create(experiment_group=experiment_group)
    elif SearchAlgorithms.is_bo(experiment_group.search_algorithm):
        auditor.record(event_type=EXPERIMENT_GROUP_BO,
                       instance=experiment_group)
        return bo.create(experiment_group=experiment_group)
    return None
