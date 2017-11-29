# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest.mock import patch

from django.test import TestCase

from experiments.constants import ExperimentLifeCycle
from experiments.models import ExperimentStatus
from libs.redis_db import RedisExperimentStatus
from tests.factories.factory_clusters import ClusterFactory
from tests.factories.factory_experiments import ExperimentFactory
from tests.factories.factory_projects import PolyaxonSpecFactory


class TestExperimentModel(TestCase):
    def test_experiment_creation_triggers_status_creation_mocks(self):
        with patch('projects.tasks.start_group_experiments.delay') as _:
            cluster = ClusterFactory()
            spec = PolyaxonSpecFactory(user=cluster.user)

        with patch('experiments.tasks.start_experiment.delay') as mock_fct:
            with patch.object(RedisExperimentStatus, 'set_status') as mock_fct2:
                ExperimentFactory(spec=spec)

        assert mock_fct.call_count == 0
        assert mock_fct2.call_count == 1

    def test_experiment_creation_triggers_status_creation(self):
        with patch('projects.tasks.start_group_experiments.delay') as _:
            cluster = ClusterFactory()
            spec = PolyaxonSpecFactory(user=cluster.user)

        experiment = ExperimentFactory(spec=spec)

        assert ExperimentStatus.objects.filter(experiment=experiment).count() == 1
        assert experiment.last_status.status == ExperimentLifeCycle.CREATED

    def test_independent_experiment_creation_triggers_experiment_scheduling_mocks(self):
        with patch('projects.tasks.start_group_experiments.delay') as _:
            with patch('experiments.tasks.start_experiment.delay') as mock_fct:
                with patch.object(RedisExperimentStatus, 'set_status') as mock_fct2:
                    ExperimentFactory()

        assert mock_fct.call_count == 1
        assert mock_fct2.call_count == 1

    def test_independent_experiment_creation_triggers_experiment_scheduling(self):
        experiment = ExperimentFactory()

        assert ExperimentStatus.objects.filter(experiment=experiment).count() == 2
        assert list(ExperimentStatus.objects.filter(experiment=experiment).values_list(
            'status', flat=True)) == ['Created', 'Scheduled']
        assert experiment.last_status.status == ExperimentLifeCycle.SCHEDULED
