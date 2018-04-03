from unittest.mock import patch

import os

from experiments.paths import (
    get_experiment_logs_path,
    get_experiment_outputs_path,
    create_experiment_outputs_path,
)
from factories.factory_experiments import ExperimentFactory
from factories.factory_experiment_groups import ExperimentGroupFactory
from experiment_groups.paths import (
    get_experiment_group_logs_path,
    delete_experiment_group_logs,
    get_experiment_group_outputs_path,
    delete_experiment_group_outputs,
)
from tests.utils import BaseTest


class TestExperimentGroupUtils(BaseTest):
    def setUp(self):
        super().setUp()
        with patch('experiment_groups.tasks.start_group_experiments.apply_async') as _:
            self.experiment_group = ExperimentGroupFactory()
        self.project = self.experiment_group.project

    def test_experiment_group_logs_path_creation_deletion(self):
        with patch('experiments.tasks.build_experiment.apply_async') as _:
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
        with patch('experiments.tasks.build_experiment.apply_async') as _:
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
