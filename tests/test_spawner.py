# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
from unittest import TestCase

from polyaxon_spawner.spawner import K8SPolyaxonFileSpawner
from tests import base


class TestPolyaxonSpawner(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = base.get_e2e_configuration()

    def test_spawner(self):
        k8s_spawner = K8SPolyaxonFileSpawner(os.path.abspath('tests/fixtures/experiment_file.yml'),
                                             self.config)
        assert k8s_spawner.project_name == k8s_spawner.spec.project.name
        k8s_spawner.start_experiment()
        k8s_spawner.delete_experiment()
