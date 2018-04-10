from unittest.mock import patch

from django.test import tag, override_settings

from experiment_groups.tasks import stop_group_experiments
from experiments.models import Experiment, ExperimentMetric
from experiments.statuses import ExperimentLifeCycle
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import ExperimentFactory, ExperimentStatusFactory
from factories.fixtures import experiment_group_spec_content_early_stopping
from tests.utils import BaseTest, RUNNER_TEST


class TestExperimentGroupModel(BaseTest):
    @override_settings(DEPLOY_RUNNER=False)
    @patch('experiment_groups.paths.delete_path')
    def test_experiment_group_creation_deletes_old_data(self, delete_path):
        ExperimentGroupFactory()

        assert delete_path.call_count == 2  # outputs + logs

    @override_settings(DEPLOY_RUNNER=False)
    @patch('experiment_groups.paths.delete_path')
    def test_experiment_group_deletion_deletes_old_data(self, delete_path):
        experiment_group = ExperimentGroupFactory()
        assert delete_path.call_count == 2  # outputs + logs
        experiment_group.delete()
        assert delete_path.call_count == 2 + 2  # outputs + logs

    @tag(RUNNER_TEST)
    def test_spec_creation_triggers_experiments_planning(self):
        with patch('experiment_groups.tasks.create_group_experiments.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory()

        assert Experiment.objects.filter(experiment_group=experiment_group).count() == 0
        assert mock_fct.call_count == 1

    @tag(RUNNER_TEST)
    def test_spec_creation_triggers_experiments_creations_and_scheduling(self):
        with patch('experiment_groups.tasks.start_group_experiments.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory()

        assert Experiment.objects.filter(experiment_group=experiment_group).count() == 2
        assert mock_fct.call_count == 1
        assert experiment_group.pending_experiments.count() == 2
        assert experiment_group.running_experiments.count() == 0
        experiment = Experiment.objects.filter(experiment_group=experiment_group).first()
        ExperimentStatusFactory(experiment=experiment, status=ExperimentLifeCycle.RUNNING)
        assert experiment_group.pending_experiments.count() == 1
        assert experiment_group.running_experiments.count() == 1

    @tag(RUNNER_TEST)
    def test_experiment_group_deletion_triggers_experiments_deletion(self):
        with patch('experiment_groups.tasks.start_group_experiments.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory()

        assert mock_fct.call_count == 1

        assert Experiment.objects.filter(experiment_group=experiment_group).count() == 2

        with patch('runner.schedulers.experiment_scheduler.stop_experiment') as mock_fct:
            experiment_group.delete()

        assert mock_fct.call_count == 2

        assert Experiment.objects.filter(experiment_group=experiment_group).count() == 0

    @tag(RUNNER_TEST)
    def test_experiment_create_a_max_of_experiments(self):
        with patch('experiment_groups.tasks.start_group_experiments.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory(
                content=experiment_group_spec_content_early_stopping)

        assert mock_fct.call_count == 1
        assert experiment_group.specification.matrix_space == 3
        assert experiment_group.experiments.count() == 2

    @tag(RUNNER_TEST)
    def test_experiment_group_should_stop_early(self):
        with patch('experiment_groups.tasks.start_group_experiments.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory(
                content=experiment_group_spec_content_early_stopping)

        assert mock_fct.call_count == 1
        assert experiment_group.should_stop_early() is False
        assert experiment_group.pending_experiments.count() == 2

        # Make a metric for one of the experiments
        experiment1, experiment2 = list(experiment_group.experiments.all())
        metric1 = ExperimentMetric.objects.create(experiment=experiment1,
                                                  values={'precision': 0.99})

        # Check again that early stopping works
        assert experiment_group.should_stop_early() is True

        # Add another metric
        metric2 = ExperimentMetric.objects.create(experiment=experiment2,
                                                  values={'loss': 0.01})

        # Check again that early stopping still works
        assert experiment_group.should_stop_early() is True

        # Delete metric1
        metric1.delete()

        # Check again that early stopping still works
        assert experiment_group.should_stop_early() is True

        # Delete metric2
        metric2.delete()

        # Check again that early stopping still works
        assert experiment_group.should_stop_early() is False

    @tag(RUNNER_TEST)
    def test_stop_pending_experiments(self):
        with patch('experiment_groups.tasks.start_group_experiments.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory(
                content=experiment_group_spec_content_early_stopping)

        assert mock_fct.call_count == 1
        assert experiment_group.pending_experiments.count() == 2

        stop_group_experiments(experiment_group_id=experiment_group.id, pending=True)

        assert experiment_group.pending_experiments.count() == 0

    @tag(RUNNER_TEST)
    def test_stop_all_experiments(self):
        with patch('experiment_groups.tasks.start_group_experiments.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory(
                content=experiment_group_spec_content_early_stopping)

        assert mock_fct.call_count == 1

        # Add a running experiment
        experiment = ExperimentFactory(experiment_group=experiment_group)
        ExperimentStatusFactory(experiment=experiment, status=ExperimentLifeCycle.RUNNING)
        assert experiment_group.pending_experiments.count() == 2
        assert experiment_group.running_experiments.count() == 1
        assert experiment_group.experiments.count() == 3
        assert experiment_group.stopped_experiments.count() == 0

        with patch('runner.schedulers.experiment_scheduler.stop_experiment') as spawner_mock_fct:
            stop_group_experiments(experiment_group_id=experiment_group.id, pending=False)

        assert experiment_group.pending_experiments.count() == 0
        assert experiment_group.running_experiments.count() == 1
        assert spawner_mock_fct.call_count == 1  # Should be stopped with ths function
        assert experiment_group.stopped_experiments.count() == 2
