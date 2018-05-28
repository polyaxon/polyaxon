import os

from unittest.mock import patch

import pytest

from factories.factory_experiments import ExperimentFactory
from factories.factory_projects import ProjectFactory
from factories.factory_repos import RepoFactory
from libs.paths.experiments import (
    create_experiment_outputs_path,
    get_experiment_logs_path,
    get_experiment_outputs_path
)
from libs.paths.projects import (
    delete_project_logs,
    delete_project_outputs,
    get_project_logs_path,
    get_project_outputs_path
)
from tests.utils import BaseTest


@pytest.mark.projects_mark
class TestProjectUtils(BaseTest):
    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.repo = RepoFactory(project=self.project)

    def test_project_logs_path_creation_deletion(self):
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as _:  # noqa
            experiment = ExperimentFactory(user=self.project.user, project=self.project)
        experiment_logs_path = get_experiment_logs_path(experiment.unique_name)
        open(experiment_logs_path, '+w')
        project_logs_path = get_project_logs_path(self.project.unique_name)
        project_repos_path = get_project_logs_path(self.project.unique_name)
        # Should be true, created by the signal
        assert os.path.exists(experiment_logs_path) is True
        assert os.path.exists(project_logs_path) is True
        assert os.path.exists(project_repos_path) is True
        delete_project_logs(self.project.unique_name)
        assert os.path.exists(experiment_logs_path) is False
        assert os.path.exists(project_logs_path) is False
        assert os.path.exists(project_repos_path) is False

    def test_project_outputs_path_creation_deletion(self):
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as _:  # noqa
            experiment = ExperimentFactory(user=self.project.user, project=self.project)
        create_experiment_outputs_path(experiment.unique_name)
        experiment_outputs_path = get_experiment_outputs_path(experiment.unique_name)
        project_outputs_path = get_project_outputs_path(self.project.unique_name)
        assert os.path.exists(experiment_outputs_path) is True
        assert os.path.exists(project_outputs_path) is True
        delete_project_outputs(self.project.unique_name)
        assert os.path.exists(experiment_outputs_path) is False
        assert os.path.exists(project_outputs_path) is False
