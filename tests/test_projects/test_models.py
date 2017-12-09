# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest.mock import patch

from experiments.models import Experiment
from factories.factory_clusters import ClusterFactory
from factories.factory_projects import ExperimentGroupFactory, ProjectFactory
from factories.factory_repos import RepoFactory
from tests.utils import BaseTest


class TestExperimentGroupModel(BaseTest):
    def test_spec_creation_triggers_experiments_creations_and_scheduling(self):
        with patch('projects.tasks.start_group_experiments.delay') as mock_fct:
            cluster = ClusterFactory()
            experiment_group = ExperimentGroupFactory(user=cluster.user)

        assert Experiment.objects.filter(experiment_group=experiment_group).count() == 1
        assert mock_fct.call_count == 1


class TestProjectModel(BaseTest):
    def test_has_code(self):
        project = ProjectFactory()
        assert project.has_code is False

        RepoFactory(project=project)
        assert project.has_code is True
