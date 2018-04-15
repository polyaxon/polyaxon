from django.test import override_settings

from experiment_groups.iteration_managers import (
    HyperbandIterationManager,
    get_search_iteration_manager
)
from experiment_groups.models import ExperimentGroupIteration
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
        assert get_search_iteration_manager(experiment_group) is None

        # Random search
        experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_early_stopping)
        assert get_search_iteration_manager(experiment_group) is None

        # Hyperband
        experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_hyperband)
        assert isinstance(get_search_iteration_manager(experiment_group), HyperbandIterationManager)


@override_settings(DEPLOY_RUNNER=False)
class TestHyperbandIterationManagers(BaseTest):
    def setUp(self):
        super().setUp()
        self.experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_hyperband)
        [ExperimentFactory(experiment_group=self.experiment_group) for _ in range(3)]
        self.iteration_manager = HyperbandIterationManager(experiment_group=self.experiment_group)

    def test_create_iteration(self):
        assert ExperimentGroupIteration.objects.count() == 0
        experiment_ids = [self.experiment_group.experiments.first().id]
        iteration = self.iteration_manager.create_iteration(experiment_ids=experiment_ids)
        assert isinstance(iteration, ExperimentGroupIteration)
        assert ExperimentGroupIteration.objects.count() == 1
        assert iteration.experiment_group == self.experiment_group
        assert iteration.data == {
            'iteration': 1,
            'bracket_iteration': 0,
            'experiment_ids': experiment_ids,
            'experiments_metrics': None,
        }
