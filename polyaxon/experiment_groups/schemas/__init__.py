from polyaxon_schemas.utils import SearchAlgorithms

from experiment_groups.schemas.hyperband import HyperbandIterationConfig


def get_iteration_config(search_algorithm, iteration=None):
    if SearchAlgorithms.is_hyperband(search_algorithm):
        if not iteration:
            raise ValueError('No iteration was provided')
        return HyperbandIterationConfig.from_dict(iteration)

    return None
