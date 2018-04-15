from django.test import override_settings

from experiment_groups.schemas import HyperbandIterationConfig, get_iteration_config
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.fixtures import (
    experiment_group_spec_content_early_stopping,
    experiment_group_spec_content_hyperband
)
from tests.utils import BaseTest


@override_settings(DEPLOY_RUNNER=False)
class TestSearchManagers(BaseTest):
    def test_get_search_algorithm_manager(self):
        # Grid search
        experiment_group = ExperimentGroupFactory()
        assert get_iteration_config(experiment_group.search_algorithm) is None

        # Random search
        experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_early_stopping)
        assert get_iteration_config(experiment_group.search_algorithm) is None

        # Hyperband
        experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_hyperband)
        iteration = {
            'iteration': 1,
            'bracket_iteration': 0,
            'experiment_ids': [1, 2, 3],
            'experiments_metrics': None
        }
        assert isinstance(get_iteration_config(experiment_group.search_algorithm,
                                               iteration=iteration),
                          HyperbandIterationConfig)


@override_settings(DEPLOY_RUNNER=False)
class TestHyperbandIterationConfig(BaseTest):
    def test_hyperband_iteration_config(self):
        config = {
            'iteration': 1,
            'bracket_iteration': 0,
            'experiment_ids': [1, 2, 3],
            'experiments_metrics': [
                ['loss', 0.5],
                ['accuracy', 0.8]
            ],
        }

        assert HyperbandIterationConfig.from_dict(config).to_dict() == config
