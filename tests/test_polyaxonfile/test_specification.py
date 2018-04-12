# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile.specification import ExperimentSpecification, PluginSpecification
from polyaxon_schemas.utils import TaskType


class TestSpecifications(TestCase):
    def test_plugin_specification_raises_for_invalid_run_section(self):
        with self.assertRaises(PolyaxonConfigurationError):
            PluginSpecification.read(os.path.abspath(
                'tests/fixtures/plugin_missing_run_exec.yml'))

        with self.assertRaises(PolyaxonConfigurationError):
            PluginSpecification.read(os.path.abspath(
                'tests/fixtures/plugin_run_exec_simple_file_with_cmd.yml'))

    def test_cluster_def_without_framwork(self):
        spec = ExperimentSpecification.read(os.path.abspath('tests/fixtures/env_without_framework.yml'))
        self.assertEqual(spec.cluster_def, ({TaskType.MASTER: 1}, False))
