import os

import pytest

import stores

from factories.factory_experiments import ExperimentFactory
from scheduler.tasks.storage import stores_schedule_logs_deletion, stores_schedule_outputs_deletion
from tests.utils import BaseTest


@pytest.mark.paths_mark
class TestExperimentPaths(BaseTest):
    def setUp(self):
        super().setUp()
        self.experiment = ExperimentFactory()

    def test_experiment_logs_path_creation_deletion(self):
        stores.create_experiment_logs_path(experiment_name=self.experiment.unique_name, temp=False)
        experiment_logs_path = stores.get_experiment_logs_path(
            experiment_name=self.experiment.unique_name,
            temp=False)
        filepath = stores.get_experiment_logs_path(
            experiment_name=self.experiment.unique_name,
            temp=False)
        open(filepath, '+w')
        assert os.path.exists(experiment_logs_path) is True
        assert os.path.exists(filepath) is True
        stores_schedule_logs_deletion(persistence=None, subpath=self.experiment.subpath)
        assert os.path.exists(filepath) is False

    def test_experiment_outputs_path_creation_deletion(self):
        experiment_outputs_path = stores.get_experiment_outputs_path(
            persistence=self.experiment.persistence_outputs,
            experiment_name=self.experiment.unique_name)
        assert os.path.exists(experiment_outputs_path) is False
        stores.create_experiment_outputs_path(
            persistence=self.experiment.persistence_outputs,
            experiment_name=self.experiment.unique_name)
        assert os.path.exists(experiment_outputs_path) is True
        stores_schedule_outputs_deletion(persistence='outputs', subpath=self.experiment.subpath)
        assert os.path.exists(experiment_outputs_path) is False
