import os

from unittest.mock import patch

import pytest

import stores

from factories.factory_experiments import ExperimentFactory
from factories.factory_projects import ProjectFactory
from factories.factory_repos import RepoFactory
from libs.paths.projects import delete_project_repos, get_project_repos_path
from scheduler.tasks.storage import stores_schedule_logs_deletion, stores_schedule_outputs_deletion
from tests.utils import BaseTest


@pytest.mark.paths_mark
class TestProjectPaths(BaseTest):
    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.repo = RepoFactory(project=self.project)

    def test_project_logs_path_creation_deletion(self):
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as _:  # noqa
            experiment = ExperimentFactory(user=self.project.user, project=self.project)
        experiment_logs_path = stores.get_experiment_logs_path(
            experiment_name=experiment.unique_name,
            temp=False)
        stores.create_experiment_logs_path(experiment_name=experiment.unique_name, temp=False)
        open(experiment_logs_path, '+w')
        project_logs_path = stores.get_project_logs_path(project_name=self.project.unique_name)
        project_repos_path = get_project_repos_path(self.project.unique_name)
        # Should be true, created by the signal
        assert os.path.exists(experiment_logs_path) is True
        assert os.path.exists(project_logs_path) is True
        assert os.path.exists(project_repos_path) is True
        stores_schedule_logs_deletion(persistence=None, subpath=self.project.subpath)
        delete_project_repos(self.project.unique_name)
        assert os.path.exists(experiment_logs_path) is False
        assert os.path.exists(project_logs_path) is False
        assert os.path.exists(project_repos_path) is False

    def test_project_outputs_path_creation_deletion(self):
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as _:  # noqa
            experiment = ExperimentFactory(user=self.project.user, project=self.project)
        stores.create_experiment_outputs_path(
            persistence=experiment.persistence_outputs,
            experiment_name=experiment.unique_name)
        experiment_outputs_path = stores.get_experiment_outputs_path(
            persistence=experiment.persistence_outputs,
            experiment_name=experiment.unique_name)
        project_outputs_path = stores.get_project_outputs_path(
            persistence=None,
            project_name=self.project.unique_name)
        assert os.path.exists(experiment_outputs_path) is True
        assert os.path.exists(project_outputs_path) is True
        stores_schedule_outputs_deletion(persistence='outputs', subpath=self.project.subpath)
        assert os.path.exists(experiment_outputs_path) is False
        assert os.path.exists(project_outputs_path) is False
