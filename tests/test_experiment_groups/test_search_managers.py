import math

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


@override_settings(DEPLOY_RUNNER=False)
class TestHyperbandSearchManager(BaseTest):
    def setUp(self):
        params_config = SettingsConfig.from_dict({
            'concurrency': 2,
            'hyperband': {
                'max_iter': 10,
                'eta': 3,
                'resource': 'steps',
                'resume': False,
                'metric': {'name': 'loss', 'optimization': 'minimize'}
            },
            'matrix': {
                'feature1': {'values': [1, 2, 3]},
                'feature2': {'linspace': [1, 2, 5]},
                'feature3': {'range': [1, 5, 1]}
            }
        })
        self.manager1 = HyperbandSearchManager(params_config=params_config)

    @staticmethod
    def almost_equal(value, value_compare):
        assert value_compare - 0.02 <= value <= value_compare + 0.02

    def test_hyperband_properties(self):
        assert self.manager1.max_iter == 10
        assert self.manager1.eta == 3
        assert self.manager1.s_max == 3
        assert self.manager1.B == self.manager1.s_max * self.manager1.max_iter

    def test_get_bracket(self):
        assert self.manager1.get_bracket(iteration=0) == 3
        assert self.manager1.get_bracket(iteration=1) == 2
        assert self.manager1.get_bracket(iteration=2) == 1
        assert self.manager1.get_bracket(iteration=3) == 0

    def test_get_n_configs(self):
        assert self.manager1.get_n_configs(bracket=3) == 21
        assert self.manager1.get_n_configs(bracket=2) == 9
        assert self.manager1.get_n_configs(bracket=1) == 5
        assert self.manager1.get_n_configs(bracket=0) == 3

    def test_get_resources(self):
        # Number of resources [/bracket, /iteration]
        self.almost_equal(self.manager1.get_resources(bracket=3), 0.37)
        self.almost_equal(self.manager1.get_resources(bracket=2), 1.11)
        self.almost_equal(self.manager1.get_resources(bracket=1), 3.33)
        self.almost_equal(self.manager1.get_resources(bracket=0), 10)

        self.almost_equal(self.manager1.get_resources_for_iteration(iteration=0), 0.37)
        self.almost_equal(self.manager1.get_resources_for_iteration(iteration=2), 3.33)
        self.almost_equal(self.manager1.get_resources_for_iteration(iteration=1), 1.11)
        self.almost_equal(self.manager1.get_resources_for_iteration(iteration=3), 10)

    def test_get_n_configs_to_keep(self):
        # Number of config to keep [/n_suggestions, /iteration]

        # Iteration == 0
        assert self.manager1.get_n_config_to_keep(n_suggestions=21,
                                                  bracket_iteration=0) == 7
        assert self.manager1.get_n_config_to_keep(n_suggestions=21,
                                                  bracket_iteration=1) == 2
        assert self.manager1.get_n_config_to_keep(n_suggestions=21,
                                                  bracket_iteration=2) == 0
        assert self.manager1.get_n_config_to_keep(n_suggestions=21,
                                                  bracket_iteration=3) == 0

        assert self.manager1.get_n_config_to_keep_for_iteration(iteration=0,
                                                                bracket_iteration=0) == 7
        assert self.manager1.get_n_config_to_keep_for_iteration(iteration=0,
                                                                bracket_iteration=1) == 2
        assert self.manager1.get_n_config_to_keep_for_iteration(iteration=0,
                                                                bracket_iteration=2) == 0
        assert self.manager1.get_n_config_to_keep_for_iteration(iteration=0,
                                                                bracket_iteration=3) == 0

        # Iteration == 1
        assert self.manager1.get_n_config_to_keep(n_suggestions=9, bracket_iteration=0) == 3
        assert self.manager1.get_n_config_to_keep(n_suggestions=9, bracket_iteration=1) == 1
        assert self.manager1.get_n_config_to_keep(n_suggestions=9, bracket_iteration=2) == 0

        assert self.manager1.get_n_config_to_keep_for_iteration(iteration=1,
                                                                bracket_iteration=0) == 3
        assert self.manager1.get_n_config_to_keep_for_iteration(iteration=1,
                                                                bracket_iteration=1) == 1
        assert self.manager1.get_n_config_to_keep_for_iteration(iteration=1,
                                                                bracket_iteration=2) == 0

        # Iteration == 2
        assert self.manager1.get_n_config_to_keep(n_suggestions=5, bracket_iteration=0) == 1
        assert self.manager1.get_n_config_to_keep(n_suggestions=5, bracket_iteration=1) == 0

        assert self.manager1.get_n_config_to_keep_for_iteration(iteration=2,
                                                                bracket_iteration=0) == 1
        assert self.manager1.get_n_config_to_keep_for_iteration(iteration=2,
                                                                bracket_iteration=1) == 0

        # Iteration == 3
        assert self.manager1.get_n_config_to_keep(n_suggestions=3, bracket_iteration=0) == 1
        assert self.manager1.get_n_config_to_keep_for_iteration(iteration=3,
                                                                bracket_iteration=0) == 1

    def test_get_n_resources(self):
        # Number of iteration resources

        # Iteration == 0
        self.almost_equal(
            self.manager1.get_n_resources(n_resources=0.37, bracket_iteration=0), 0.37)
        self.almost_equal(
            self.manager1.get_n_resources(n_resources=0.37, bracket_iteration=1), 1.1)
        self.almost_equal(
            self.manager1.get_n_resources(n_resources=0.37, bracket_iteration=2), 3.33)
        self.almost_equal(
            self.manager1.get_n_resources(n_resources=0.37, bracket_iteration=3), 9.99)

        self.almost_equal(
            self.manager1.get_n_resources_for_iteration(
                iteration=0, bracket_iteration=0), 0.37)
        self.almost_equal(
            self.manager1.get_n_resources_for_iteration(
                iteration=0, bracket_iteration=1), 1.1)
        self.almost_equal(
            self.manager1.get_n_resources_for_iteration(
                iteration=0, bracket_iteration=2), 3.33)
        self.almost_equal(
            self.manager1.get_n_resources_for_iteration(
                iteration=0, bracket_iteration=3), 9.99)

        # Iteration == 1
        self.almost_equal(
            self.manager1.get_n_resources(n_resources=1.11, bracket_iteration=0), 1.11)
        self.almost_equal(
            self.manager1.get_n_resources(n_resources=1.11, bracket_iteration=1), 3.33)
        self.almost_equal(
            self.manager1.get_n_resources(n_resources=1.11, bracket_iteration=2), 9.99)

        self.almost_equal(
            self.manager1.get_n_resources_for_iteration(
                iteration=1, bracket_iteration=0), 1.11)
        self.almost_equal(
            self.manager1.get_n_resources_for_iteration(
                iteration=1, bracket_iteration=1), 3.33)
        self.almost_equal(
            self.manager1.get_n_resources_for_iteration(
                iteration=1, bracket_iteration=2), 9.99)

        # Iteration == 2
        self.almost_equal(
            self.manager1.get_n_resources(n_resources=3.33, bracket_iteration=0), 3.33)
        self.almost_equal(
            self.manager1.get_n_resources(n_resources=3.33, bracket_iteration=1), 9.99)

        self.almost_equal(
            self.manager1.get_n_resources_for_iteration(
                iteration=2, bracket_iteration=0), 3.33)
        self.almost_equal(
            self.manager1.get_n_resources_for_iteration(
                iteration=2, bracket_iteration=1), 9.99)

        # Iteration == 3
        self.almost_equal(
            self.manager1.get_n_resources(n_resources=10, bracket_iteration=0), 10)

        self.almost_equal(
            self.manager1.get_n_resources_for_iteration(
                iteration=3, bracket_iteration=0), 10)
