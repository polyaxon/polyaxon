from suggester.schemas.bayesian_optimization import BOIterationConfig
from suggester.schemas.hyperband import HyperbandIterationConfig
from polyaxon_schemas.utils import SearchAlgorithms


def get_iteration_config(search_algorithm, iteration=None):
    if SearchAlgorithms.is_hyperband(search_algorithm):
        if not iteration:
            raise ValueError('No iteration was provided')
        return HyperbandIterationConfig.from_dict(iteration)
    if SearchAlgorithms.is_bo(search_algorithm):
        if not iteration:
            raise ValueError('No iteration was provided')
        return BOIterationConfig.from_dict(iteration)
    return None
