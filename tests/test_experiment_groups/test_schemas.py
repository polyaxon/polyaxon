import pytest

from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.fixtures import (
    experiment_group_spec_content_bo,
    experiment_group_spec_content_early_stopping,
    experiment_group_spec_content_hyperband
)
from hpsearch.schemas import (
    BaseIterationConfig,
    BOIterationConfig,
    HyperbandIterationConfig,
    get_iteration_config
)
from tests.utils import BaseTest


@pytest.mark.experiment_groups_mark
class TestSearchManagers(BaseTest):
    def test_get_search_algorithm_manager(self):
        iteration = {
            'iteration': 1,
            'num_suggestions': 12,
        }
        # Grid search
        experiment_group = ExperimentGroupFactory()
        assert isinstance(get_iteration_config(experiment_group.search_algorithm,
                                               iteration=iteration),
                          BaseIterationConfig)

        # Random search
        experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_early_stopping)
        assert isinstance(get_iteration_config(experiment_group.search_algorithm,
                                               iteration=iteration),
                          BaseIterationConfig)

        # Hyperband
        experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_hyperband)
        iteration = {
            'iteration': 1,
            'num_suggestions': 12,
            'bracket_iteration': 0,
            'experiment_ids': [1, 2, 3],
            'experiments_metrics': None
        }
        assert isinstance(get_iteration_config(experiment_group.search_algorithm,
                                               iteration=iteration),
                          HyperbandIterationConfig)

        # BO
        experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_bo)
        iteration = {
            'iteration': 1,
            'num_suggestions': 12,
            'experiment_ids': [1, 2, 3],
            'experiment_configs': [[1, {1: 1}], [2, {2: 2}], [3, {3: 3}]],
            'experiments_metrics': None
        }
        assert isinstance(get_iteration_config(experiment_group.search_algorithm,
                                               iteration=iteration),
                          BOIterationConfig)


@pytest.mark.experiment_groups_mark
class TestaseIterationConfig(BaseTest):
    DISABLE_RUNNER = True
    DISABLE_EXECUTOR = True

    def test_base_iteration_config(self):
        config = {
            'iteration': 1,
            'num_suggestions': 10,
            'experiment_ids': [1, 2, 3],
        }

        assert BaseIterationConfig.from_dict(config).to_dict() == config


@pytest.mark.experiment_groups_mark
class TestHyperbandIterationConfig(BaseTest):
    DISABLE_RUNNER = True
    DISABLE_EXECUTOR = True

    def test_hyperband_iteration_config(self):
        config = {
            'iteration': 1,
            'num_suggestions': 10,
            'bracket_iteration': 0,
            'experiment_ids': [1, 2, 3],
            'experiments_metrics': [[1, 0.5], [2, 0.8], [3, 0.8]],
        }

        assert HyperbandIterationConfig.from_dict(config).to_dict() == config


@pytest.mark.experiment_groups_mark
class TestBOIterationConfig(BaseTest):
    def test_bo_iteration_config(self):
        config = {
            'iteration': 2,
            'num_suggestions': 10,
            'experiment_ids': [5, 6, 7],
            'experiments_configs': [
                [5, {'param1': 0.5}], [6, {'param1': 0.5}], [7, {'param1': 0.5}]],
            'experiments_metrics': [
                [5, 0.5], [6, 0.8], [7, 0.8]],
            'old_experiment_ids': [1, 2, 3],
            'old_experiments_configs': [
                [1, {'param1': 0.5}], [2, {'param1': 0.5}], [3, {'param1': 0.5}]],
            'old_experiments_metrics': [
                [1, 0.5], [2, 0.8], [3, 0.8]],
        }

        assert BOIterationConfig.from_dict(config).to_dict() == config
