import pytest

from flaky import flaky

from db.models.experiment_groups import ExperimentGroupIteration
from db.models.experiments import ExperimentMetric
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import ExperimentFactory
from factories.fixtures import (
    experiment_group_spec_content_2_xps,
    experiment_group_spec_content_bo,
    experiment_group_spec_content_early_stopping,
    experiment_group_spec_content_hyperband
)
from hpsearch.iteration_managers import (
    BaseIterationManager,
    BOIterationManager,
    HyperbandIterationManager,
    get_search_iteration_manager
)
from tests.utils import BaseTest


@pytest.mark.experiment_groups_mark
class TestIterationManagers(BaseTest):
    def test_get_search_iteration_manager(self):
        # Grid search
        experiment_group = ExperimentGroupFactory()
        assert isinstance(get_search_iteration_manager(experiment_group), BaseIterationManager)

        # Random search
        experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_early_stopping)
        assert isinstance(get_search_iteration_manager(experiment_group), BaseIterationManager)

        # Hyperband
        experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_hyperband)
        assert isinstance(get_search_iteration_manager(experiment_group), HyperbandIterationManager)

        # BO
        experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_bo)
        assert isinstance(get_search_iteration_manager(experiment_group), BOIterationManager)


@pytest.mark.experiment_groups_mark
class TestBaseIterationManagers(BaseTest):
    def setUp(self):
        super().setUp()
        self.experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_2_xps)
        for _ in range(3):
            ExperimentFactory(experiment_group=self.experiment_group)
        self.iteration_manager = BaseIterationManager(experiment_group=self.experiment_group)

    @flaky(max_runs=3)
    def test_create_iteration(self):
        assert ExperimentGroupIteration.objects.count() == 0
        experiment_ids = [self.experiment_group.experiments.first().id]
        iteration = self.iteration_manager.create_iteration(num_suggestions=10)
        assert isinstance(iteration, ExperimentGroupIteration)
        assert ExperimentGroupIteration.objects.count() == 1
        assert iteration.experiment_group == self.experiment_group
        assert self.experiment_group.iteration_data == {
            'num_suggestions': 10,
            'iteration': 0,
            'experiment_ids': [],
        }
        self.iteration_manager.add_iteration_experiments(experiment_ids=experiment_ids)
        assert self.experiment_group.iteration_data == {
            'num_suggestions': 10,
            'iteration': 0,
            'experiment_ids': experiment_ids,
        }
        self.iteration_manager.add_iteration_experiments(experiment_ids=experiment_ids)
        assert self.experiment_group.iteration_data == {
            'num_suggestions': 10,
            'iteration': 0,
            'experiment_ids': experiment_ids,
        }
        self.iteration_manager.update_iteration_num_suggestions(num_suggestions=3)
        assert self.experiment_group.iteration_data == {
            'num_suggestions': 3,
            'iteration': 0,
            'experiment_ids': experiment_ids,
        }
        experiment_ids = list(self.experiment_group.experiments.values_list('id', flat=True))
        self.iteration_manager.add_iteration_experiments(experiment_ids=experiment_ids)
        self.assertEqual(sorted(self.experiment_group.iteration_data['experiment_ids']),
                         sorted(experiment_ids))

    def test_update_iteration_raises_if_not_iteration_is_created(self):
        self.iteration_manager.update_iteration()
        assert ExperimentGroupIteration.objects.count() == 0


@pytest.mark.experiment_groups_mark
class TestHyperbandIterationManagers(BaseTest):
    def setUp(self):
        super().setUp()
        self.experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_hyperband)
        for _ in range(3):
            ExperimentFactory(experiment_group=self.experiment_group)
        self.iteration_manager = HyperbandIterationManager(experiment_group=self.experiment_group)

    @flaky(max_runs=3)
    def test_create_iteration(self):
        assert ExperimentGroupIteration.objects.count() == 0
        experiment_ids = [self.experiment_group.experiments.first().id]
        iteration = self.iteration_manager.create_iteration()
        assert isinstance(iteration, ExperimentGroupIteration)
        assert ExperimentGroupIteration.objects.count() == 1
        assert iteration.experiment_group == self.experiment_group
        assert iteration.data == {
            'iteration': 0,
            'num_suggestions': 0,
            'bracket_iteration': 0,
            'experiment_ids': [],
            'experiments_metrics': None,
        }
        self.iteration_manager.add_iteration_experiments(experiment_ids=experiment_ids)
        assert self.experiment_group.iteration_data == {
            'iteration': 0,
            'bracket_iteration': 0,
            'num_suggestions': 0,
            'experiment_ids': experiment_ids,
            'experiments_metrics': None,
        }
        self.iteration_manager.add_iteration_experiments(experiment_ids=experiment_ids)
        assert self.experiment_group.iteration_data == {
            'iteration': 0,
            'bracket_iteration': 0,
            'num_suggestions': 0,
            'experiment_ids': experiment_ids,
            'experiments_metrics': None,
        }
        self.iteration_manager.update_iteration_num_suggestions(num_suggestions=3)
        assert self.experiment_group.iteration_data == {
            'iteration': 0,
            'bracket_iteration': 0,
            'num_suggestions': 3,
            'experiment_ids': experiment_ids,
            'experiments_metrics': None,
        }
        experiment_ids = list(self.experiment_group.experiments.values_list('id', flat=True))
        self.iteration_manager.add_iteration_experiments(experiment_ids=experiment_ids)
        self.assertEqual(sorted(self.experiment_group.iteration_data['experiment_ids']),
                         sorted(experiment_ids))

    def test_update_iteration_raises_if_not_iteration_is_created(self):
        self.iteration_manager.update_iteration()
        assert ExperimentGroupIteration.objects.count() == 0

    def test_update_iteration(self):
        assert ExperimentGroupIteration.objects.count() == 0
        experiment_ids = [self.experiment_group.experiments.first().id]
        iteration = self.iteration_manager.create_iteration()
        self.iteration_manager.add_iteration_experiments(experiment_ids=experiment_ids)
        assert iteration.data['experiments_metrics'] is None
        self.iteration_manager.update_iteration()
        assert ExperimentGroupIteration.objects.count() == 1

        iteration.refresh_from_db()
        assert iteration.data['experiments_metrics'] == []

        ExperimentMetric.objects.create(
            experiment_id=experiment_ids[0],
            values={self.experiment_group.hptuning_config.hyperband.metric.name: 0.9})
        self.iteration_manager.update_iteration()
        iteration.refresh_from_db()
        assert iteration.data['experiments_metrics'] == [[experiment_ids[0], 0.9]]

    def test_get_reduced_configs(self):
        assert ExperimentGroupIteration.objects.count() == 0
        experiment_ids = [self.experiment_group.experiments.first().id]
        iteration = self.iteration_manager.create_iteration()
        self.iteration_manager.add_iteration_experiments(experiment_ids=experiment_ids)
        assert iteration.data['experiments_metrics'] is None
        self.iteration_manager.update_iteration()
        assert ExperimentGroupIteration.objects.count() == 1

        assert self.iteration_manager.get_reduced_configs() == []


@pytest.mark.experiment_groups_mark
class TestBOIterationManagers(BaseTest):
    def setUp(self):
        super().setUp()
        self.experiment_group = ExperimentGroupFactory(
            content=experiment_group_spec_content_bo)
        self.experiments_iter1 = [
            ExperimentFactory(experiment_group=self.experiment_group, declarations={'i': i})
            for i in range(2)]
        self.experiments_iter2 = [
            ExperimentFactory(experiment_group=self.experiment_group, declarations={'i': i})
            for i in range(2)]
        self.experiments_iter3 = [
            ExperimentFactory(experiment_group=self.experiment_group, declarations={'i': i})
            for i in range(2)]
        self.iteration_manager = BOIterationManager(experiment_group=self.experiment_group)

    # @staticmethod
    # def assert_equal_configs(config1, config2):
    #     assert config1['iteration'] == config2['iteration']
    #     assert config1['num_suggestions'] == config2['num_suggestions']
    #     assert sorted(config1['old_experiment_ids']) == sorted(config2['old_experiment_ids'])
    #     for v in config2['old_experiments_configs']:
    #         assert v in config1['old_experiments_configs']
    #     for v in config2['old_experiments_metrics']:
    #         assert v in config1['old_experiments_metrics']
    #     assert sorted(config1['experiment_ids']) == sorted(config2['experiment_ids'])
    #     for v in config2['experiments_configs']:
    #         assert v in config1['experiments_configs']
    #     for v in config2['experiments_metrics']:
    #         assert v in config1['experiments_metrics']

    @flaky(max_runs=3)
    def test_create_iteration(self):
        assert ExperimentGroupIteration.objects.count() == 0
        assert self.experiment_group.current_iteration == 0
        experiment_iter1_ids = [experiment.id for experiment in self.experiments_iter1]
        experiments_iter1_configs = [[experiment.id, experiment.declarations]
                                     for experiment in reversed(self.experiments_iter1)]
        iteration = self.iteration_manager.create_iteration(num_suggestions=2)
        self.iteration_manager.add_iteration_experiments(experiment_ids=experiment_iter1_ids)
        assert isinstance(iteration, ExperimentGroupIteration)
        assert ExperimentGroupIteration.objects.count() == 1
        assert self.experiment_group.current_iteration == 1
        assert iteration.experiment_group == self.experiment_group
        assert self.experiment_group.iteration_data == {
            'iteration': 0,
            'num_suggestions': 2,
            'old_experiment_ids': None,
            'old_experiments_configs': None,
            'old_experiments_metrics': None,
            'experiment_ids': experiment_iter1_ids,
            'experiments_configs': [],
            'experiments_metrics': None
        }

        # Update iteration
        for experiment_id in experiment_iter1_ids:
            ExperimentMetric.objects.create(
                experiment_id=experiment_id,
                values={self.experiment_group.hptuning_config.bo.metric.name: 0.8})
        self.iteration_manager.update_iteration()
        iteration.refresh_from_db()
        experiment_iter1_metrics = [
            [experiment_id, 0.8] for experiment_id in reversed(experiment_iter1_ids)
        ]
        assert iteration.data['experiments_metrics'] == experiment_iter1_metrics

        # Creating a new iteration uses data from previous iteration
        experiment_iter2_ids = [experiment.id for experiment in self.experiments_iter2]
        experiments_iter2_configs = [[experiment.id, experiment.declarations]
                                     for experiment in reversed(self.experiments_iter2)]
        iteration = self.iteration_manager.create_iteration(num_suggestions=2)
        self.iteration_manager.add_iteration_experiments(experiment_ids=experiment_iter2_ids)
        self.iteration_manager.update_iteration()

        assert self.experiment_group.current_iteration == 2
        assert self.experiment_group.iteration_data == {
            'iteration': 1,
            'num_suggestions': 2,
            'old_experiment_ids': experiment_iter1_ids,
            'old_experiments_configs': experiments_iter1_configs,
            'old_experiments_metrics': experiment_iter1_metrics,
            'experiment_ids': experiment_iter2_ids,
            'experiments_configs': experiments_iter2_configs,
            'experiments_metrics': []
        }

        # Update iteration
        for experiment_id in experiment_iter2_ids:
            ExperimentMetric.objects.create(
                experiment_id=experiment_id,
                values={self.experiment_group.hptuning_config.bo.metric.name: 0.9})
        self.iteration_manager.update_iteration()
        iteration.refresh_from_db()
        experiment_iter2_metrics = [
            [experiment_id, 0.9] for experiment_id in reversed(experiment_iter2_ids)
        ]
        assert iteration.data['experiments_metrics'] == experiment_iter2_metrics

        # Creating a new iteration uses data from previous iteration
        experiment_iter3_ids = [experiment.id for experiment in self.experiments_iter3]
        experiments_iter3_configs = [[experiment.id, experiment.declarations]
                                     for experiment in reversed(self.experiments_iter3)]
        iteration = self.iteration_manager.create_iteration(num_suggestions=2)
        self.iteration_manager.add_iteration_experiments(experiment_ids=experiment_iter3_ids)
        self.iteration_manager.update_iteration()
        assert self.experiment_group.current_iteration == 3
        assert self.experiment_group.iteration_data == {
            'iteration': 2,
            'num_suggestions': 2,
            'old_experiment_ids': experiment_iter1_ids + experiment_iter2_ids,
            'old_experiments_configs': experiments_iter1_configs + experiments_iter2_configs,
            'old_experiments_metrics': experiment_iter1_metrics + experiment_iter2_metrics,
            'experiment_ids': experiment_iter3_ids,
            'experiments_configs': experiments_iter3_configs,
            'experiments_metrics': []
        }

        # Update iteration
        for experiment_id in experiment_iter3_ids:
            ExperimentMetric.objects.create(
                experiment_id=experiment_id,
                values={self.experiment_group.hptuning_config.bo.metric.name: 0.9})
        self.iteration_manager.update_iteration()
        iteration.refresh_from_db()
        experiment_iter3_metrics = [
            [experiment_id, 0.9] for experiment_id in reversed(experiment_iter3_ids)
        ]
        assert iteration.data['experiments_metrics'] == experiment_iter3_metrics

    def test_update_iteration_raises_if_not_iteration_is_created(self):
        self.iteration_manager.update_iteration()
        assert ExperimentGroupIteration.objects.count() == 0
