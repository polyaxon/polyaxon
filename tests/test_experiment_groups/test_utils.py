import os

from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import ExperimentFactory
from libs.paths.experiment_groups import (
    delete_experiment_group_logs,
    delete_experiment_group_outputs,
    get_experiment_group_logs_path,
    get_experiment_group_outputs_path
)
from libs.paths.experiments import (
    create_experiment_outputs_path,
    get_experiment_logs_path,
    get_experiment_outputs_path
)
from tests.utils import BaseTest


class TestExperimentGroupUtils(BaseTest):
    def setUp(self):
        super().setUp()
        self.experiment_group = ExperimentGroupFactory()
        self.project = self.experiment_group.project

    def test_experiment_group_logs_path_creation_deletion(self):
        experiment = ExperimentFactory(user=self.project.user,
                                       project=self.project,
                                       experiment_group=self.experiment_group)
        experiment_logs_path = get_experiment_logs_path(experiment.unique_name)
        open(experiment_logs_path, '+w')
        experiment_group_logs_path = get_experiment_group_logs_path(
            self.experiment_group.unique_name)
        # Should be true, created by the signal
        assert os.path.exists(experiment_logs_path) is True
        assert os.path.exists(experiment_group_logs_path) is True
        delete_experiment_group_logs(self.experiment_group.unique_name)
        assert os.path.exists(experiment_logs_path) is False
        assert os.path.exists(experiment_group_logs_path) is False

    def test_experiment_group_outputs_path_creation_deletion(self):
        experiment = ExperimentFactory(user=self.project.user,
                                       project=self.project,
                                       experiment_group=self.experiment_group)
        create_experiment_outputs_path(experiment.unique_name)
        experiment_outputs_path = get_experiment_outputs_path(experiment.unique_name)
        experiment_group_outputs_path = get_experiment_group_outputs_path(
            self.experiment_group.unique_name)
        assert os.path.exists(experiment_outputs_path) is True
        assert os.path.exists(experiment_group_outputs_path) is True
        delete_experiment_group_outputs(self.experiment_group.unique_name)
        assert os.path.exists(experiment_outputs_path) is False
        assert os.path.exists(experiment_group_outputs_path) is False
