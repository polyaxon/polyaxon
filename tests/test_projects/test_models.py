# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest.mock import patch

from experiments.models import Experiment
from tests.factories.factory_clusters import ClusterFactory
from tests.factories.factory_projects import PolyaxonSpecFactory
from tests.utils import BaseTest

class TestPolyaxonSpecModel(BaseTest):
    def test_spec_creation_triggers_experiments_creations_and_scheduling(self):
        with patch('projects.tasks.start_group_experiments.delay') as mock_fct:
            cluster = ClusterFactory()
            spec = PolyaxonSpecFactory(user=cluster.user)

        assert Experiment.objects.filter(spec=spec).count() == 1
        assert mock_fct.call_count == 1
