# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

from polyaxon_schemas.exceptions import PolyaxonConfigurationError, PolyaxonfileError
from polyaxon_schemas.polyaxonfile.specification import (
    BuildSpecification,
    ExperimentSpecification,
    PluginSpecification
)
from polyaxon_schemas.utils import TaskType


class TestSpecifications(TestCase):
    def test_plugin_specification_raises_for_invalid_run_section(self):
        with self.assertRaises(PolyaxonConfigurationError):
            PluginSpecification.read(os.path.abspath(
                'tests/fixtures/plugin_missing_run_exec.yml'))

        with self.assertRaises(PolyaxonConfigurationError):
            PluginSpecification.read(os.path.abspath(
                'tests/fixtures/plugin_run_exec_simple_file_with_cmd.yml'))

    def test_plugin_specification_raises_for_missing_build_section(self):
        with self.assertRaises(PolyaxonConfigurationError):
            BuildSpecification.read(os.path.abspath(
                'tests/fixtures/missing_build.yml'))

    def test_create_plugin_specification(self):
        run_config = {'image': 'blabla'}
        config = PluginSpecification.create_specification(run_config)
        assert PluginSpecification.read(config).parsed_data == config
        assert config['run'] == run_config

    def test_create_build_specification(self):
        # Normal build config
        build_config = {'image': 'blabla'}
        config = BuildSpecification.create_specification(build_config)
        assert BuildSpecification.read(config).parsed_data == config
        assert config['build'] == build_config

        # Run config
        run_config = {'image': 'blabla', 'cmd': 'some command'}
        import pdb; pdb.set_trace()
        config = BuildSpecification.create_specification(run_config)
        assert BuildSpecification.read(config).parsed_data == config
        assert config['build'] == {'image': 'blabla'}

    def test_cluster_def_without_framework(self):
        spec = ExperimentSpecification.read(os.path.abspath(
            'tests/fixtures/env_without_framework.yml'))
        self.assertEqual(spec.cluster_def, ({TaskType.MASTER: 1}, False))

    def test_patch(self):
        content = {
            'version': 1,
            'kind': 'experiment',
            'run': {'image': 'my_image',  'cmd': 'train'}
        }
        spec = ExperimentSpecification.read(content)
        assert spec.declarations is None

        # Add declarations
        declarations = {'declarations': {'lr': 0.1}}
        spec = spec.patch(values=declarations)
        assert spec.declarations == declarations['declarations']

        # Update declarations
        declarations = {'declarations': {'lr': 0.01, 'num_steps': 100}}
        spec = spec.patch(values=declarations)
        assert spec.declarations == declarations['declarations']

        # Add env
        assert spec.environment is None
        env = {'environment': {'resources': {'gpu': {'requests': 1, 'limits': 1}}}}
        spec = spec.patch(values=env)
        assert spec.declarations == declarations['declarations']
        assert spec.environment.resources.gpu.to_dict() == env['environment']['resources']['gpu']

        # Patch with unsupported spec
        matrix = {'settings': {'matrix': {'lr': {'values': [0.1, 0.2]}}}}
        with self.assertRaises(PolyaxonConfigurationError):
            spec.patch(values=matrix)

        # Patch with unsupported spec
        wrong_config = {'lr': {'values': [0.1, 0.2]}}
        with self.assertRaises(PolyaxonfileError):
            spec.patch(values=wrong_config)
