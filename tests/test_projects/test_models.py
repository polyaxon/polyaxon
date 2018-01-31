# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest.mock import patch

from factories.factory_experiments import ExperimentStatusFactory
from factories.factory_projects import ExperimentGroupFactory, ProjectFactory
from factories.factory_repos import RepoFactory

from spawner.utils.constants import ExperimentLifeCycle
from experiments.models import Experiment

from tests.utils import BaseTest


class TestExperimentGroupModel(BaseTest):
    def test_spec_creation_triggers_experiments_creations_and_scheduling(self):
        with patch('projects.tasks.start_group_experiments.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory()

        assert Experiment.objects.filter(experiment_group=experiment_group).count() == 2
        assert mock_fct.call_count == 1
        assert len(experiment_group.pending_experiments) == 2
        assert len(experiment_group.running_experiments) == 0
        experiment = Experiment.objects.filter(experiment_group=experiment_group).first()
        ExperimentStatusFactory(experiment=experiment, status=ExperimentLifeCycle.RUNNING)
        assert len(experiment_group.pending_experiments) == 1
        assert len(experiment_group.running_experiments) == 1

    def test_experiment_group_deletion_triggers_experiments_deletion(self):
        with patch('projects.tasks.start_group_experiments.apply_async') as mock_fct:
            experiment_group = ExperimentGroupFactory()

        assert mock_fct.call_count == 1

        assert Experiment.objects.filter(experiment_group=experiment_group).count() == 2

        with patch('spawner.scheduler.stop_experiment') as mock_fct:
            experiment_group.delete()

        assert mock_fct.call_count == 2

        assert Experiment.objects.filter(experiment_group=experiment_group).count() == 0


class TestProjectModel(BaseTest):
    def test_has_code(self):
        project = ProjectFactory()
        assert project.has_code is False

        RepoFactory(project=project)
        assert project.has_code is True
