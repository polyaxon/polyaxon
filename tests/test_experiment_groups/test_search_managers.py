from django.test import override_settings
from polyaxon_schemas.settings import SettingsConfig

from experiment_groups.iteration_managers import (
    HyperbandIterationManager,
    get_search_iteration_manager
)
from experiment_groups.models import ExperimentGroupIteration
from experiment_groups.search_managers import GridSearchManager, get_search_algorithm_manager, \
    RandomSearchManager, HyperbandSearchManager
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import ExperimentFactory
from factories.fixtures import (
    experiment_group_spec_content_early_stopping,
    experiment_group_spec_content_hyperband
)
from tests.utils import BaseTest


@override_settings(DEPLOY_RUNNER=False)
class TestIterationManagers(BaseTest):
    def test_get_search_iteration_manager(self):
        # Grid search
        experiment_group = ExperimentGroupFactory()
        assert isinstance(get_search_algorithm_manager(experiment_group.params_config),
                          GridSearchManager)

        # Random search
        experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_early_stopping)
        assert isinstance(get_search_algorithm_manager(experiment_group.params_config),
                          RandomSearchManager)

        # Hyperband
        experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_hyperband)
        assert isinstance(get_search_algorithm_manager(experiment_group.params_config),
                          HyperbandSearchManager)


@override_settings(DEPLOY_RUNNER=False)
class TestGridSearchManager(BaseTest):
    def test_get_suggestions(self):
        params_config = SettingsConfig.from_dict({
            'concurrent_experiments': 2,
            'grid_search': {'n_experiments': 10},
            'matrix': {'feature': {'values': [1, 2, 3]}}
        })
        manager = GridSearchManager(params_config=params_config)
        assert len(manager.get_suggestions()) == 3

        params_config = SettingsConfig.from_dict({
            'concurrent_experiments': 2,
            'grid_search': {'n_experiments': 10},
            'matrix': {
                'feature1': {'values': [1, 2, 3]},
                'feature2': {'linspace': [1, 2, 5]},
                'feature3': {'range': [1, 5, 1]}
            }
        })
        manager = GridSearchManager(params_config=params_config)
        assert len(manager.get_suggestions()) == 10
