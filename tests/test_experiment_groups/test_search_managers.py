from django.test import override_settings
from unittest.mock import patch

from polyaxon_schemas.matrix import MatrixConfig

from experiment_groups.search_managers import (
    GridSearchManager,
    HyperbandSearchManager,
    RandomSearchManager,
    get_search_algorithm_manager
)
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.fixtures import (
    experiment_group_spec_content_early_stopping,
    experiment_group_spec_content_hyperband
)
from polyaxon_schemas.settings import SettingsConfig
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
            'concurrency': 2,
            'grid_search': {'n_experiments': 10},
            'matrix': {'feature': {'values': [1, 2, 3]}}
        })
        manager = GridSearchManager(params_config=params_config)
        assert len(manager.get_suggestions()) == 3

        params_config = SettingsConfig.from_dict({
            'concurrency': 2,
            'grid_search': {'n_experiments': 10},
            'matrix': {
                'feature1': {'values': [1, 2, 3]},
                'feature2': {'linspace': [1, 2, 5]},
                'feature3': {'range': [1, 5, 1]}
            }
        })
        manager = GridSearchManager(params_config=params_config)
        assert len(manager.get_suggestions()) == 10

    def test_get_suggestions_calls_to_numpy(self):
        params_config = SettingsConfig.from_dict({
            'concurrency': 2,
            'grid_search': {'n_experiments': 10},
            'matrix': {'feature': {'values': [1, 2, 3]}}
        })
        manager = GridSearchManager(params_config=params_config)
        with patch.object(MatrixConfig, 'to_numpy') as to_numpy_mock:
            manager.get_suggestions()

        assert to_numpy_mock.call_count == 1

        params_config = SettingsConfig.from_dict({
            'concurrency': 2,
            'grid_search': {'n_experiments': 10},
            'matrix': {
                'feature1': {'values': [1, 2, 3]},
                'feature2': {'logspace': '0.01:0.1:5'}
            }
        })
        manager = GridSearchManager(params_config=params_config)
        with patch.object(MatrixConfig, 'to_numpy') as to_numpy_mock:
            manager.get_suggestions()

        assert to_numpy_mock.call_count == 2


@override_settings(DEPLOY_RUNNER=False)
class TestRandomSearchManager(BaseTest):
    def test_get_suggestions(self):
        params_config = SettingsConfig.from_dict({
            'concurrency': 2,
            'random_search': {'n_experiments': 10},
            'matrix': {
                'feature1': {'values': [1, 2, 3]},
                'feature2': {'linspace': [1, 2, 5]},
                'feature3': {'range': [1, 5, 1]}
            }
        })
        manager = RandomSearchManager(params_config=params_config)
        assert len(manager.get_suggestions()) == 10

        params_config = SettingsConfig.from_dict({
            'concurrency': 2,
            'random_search': {'n_experiments': 10},
            'matrix': {
                'feature1': {'pvalues': [(1, 0.3), (2, 0.3), (3, 0.3)]},
                'feature2': {'uniform': [0, 1]},
                'feature3': {'qlognormal': [0, 0.5, 0.51]}
            }
        })
        manager = RandomSearchManager(params_config=params_config)
        assert len(manager.get_suggestions()) == 10

    def test_get_suggestions_calls_sample(self):
        params_config = SettingsConfig.from_dict({
            'concurrency': 2,
            'random_search': {'n_experiments': 1},
            'matrix': {
                'feature1': {'values': [1, 2, 3]},
                'feature2': {'linspace': [1, 2, 5]},
                'feature3': {'range': [1, 5, 1]}
            }
        })
        manager = RandomSearchManager(params_config=params_config)
        with patch.object(MatrixConfig, 'sample') as sample_mock:
            manager.get_suggestions()

        assert sample_mock.call_count == 3

        params_config = SettingsConfig.from_dict({
            'concurrency': 2,
            'random_search': {'n_experiments': 1},
            'matrix': {
                'feature1': {'pvalues': [(1, 0.3), (2, 0.3), (3, 0.3)]},
                'feature2': {'uniform': [0, 1]},
                'feature3': {'qlognormal': [0, 0.5, 0.51]},
                'feature4': {'range': [1, 5, 1]}
            }
        })
        manager = RandomSearchManager(params_config=params_config)
        with patch.object(MatrixConfig, 'sample') as sample_mock:
            manager.get_suggestions()

        assert sample_mock.call_count == 4
