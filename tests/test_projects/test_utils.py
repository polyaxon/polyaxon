# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest.mock import patch

import os

from experiments.paths import (
    get_experiment_logs_path,
    get_experiment_outputs_path,
    create_experiment_outputs_path,
)
from factories.factory_experiments import ExperimentFactory
from factories.factory_projects import ProjectFactory, ExperimentGroupFactory
from factories.factory_repos import RepoFactory
from projects.paths import (
    delete_project_logs,
    get_project_logs_path,
    delete_project_outputs,
    get_experiment_group_logs_path,
    delete_experiment_group_logs,
    get_experiment_group_outputs_path,
    get_project_outputs_path,
    delete_experiment_group_outputs,
)
from tests.utils import BaseTest


class TestProjectUtils(BaseTest):
    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.repo = RepoFactory(project=self.project)

    def test_project_logs_path_creation_deletion(self):
        with patch('experiments.tasks.build_experiment.apply_async') as _:
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
        with patch('experiments.tasks.build_experiment.apply_async') as _:
            experiment = ExperimentFactory(user=self.project.user, project=self.project)
        create_experiment_outputs_path(experiment.unique_name)
        experiment_outputs_path = get_experiment_outputs_path(experiment.unique_name)
        project_outputs_path = get_project_outputs_path(self.project.unique_name)
        assert os.path.exists(experiment_outputs_path) is True
        assert os.path.exists(project_outputs_path) is True
        delete_project_outputs(self.project.unique_name)
        assert os.path.exists(experiment_outputs_path) is False
        assert os.path.exists(project_outputs_path) is False


class TestExperimentGroupUtils(BaseTest):
    def setUp(self):
        super().setUp()
        with patch('projects.tasks.start_group_experiments.apply_async') as _:
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
