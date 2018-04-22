from experiment_groups.search_managers.base import BaseSearchAlgorithmManager
from experiment_groups.search_managers.bayesian_optimization.acquisition_function import (
    UtilityFunction
)
from polyaxon_schemas.utils import SearchAlgorithms


class BOManager(BaseSearchAlgorithmManager):
    """Bayesian optimization algorithm manager for hyperparameter optimization."""

    NAME = SearchAlgorithms.BO

    def __init__(self, params_config):
        super(BOManager, self).__init__(params_config=params_config)
        self.utility_function = UtilityFunction(
            config=self.params_config.bo.utility_function, seed=params_config.seed)
