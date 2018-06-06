# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

from polyaxon_schemas.exceptions import PolyaxonConfigurationError, PolyaxonfileError
from polyaxon_schemas.polyaxonfile.specification import (
    BuildSpecification,
    ExperimentSpecification,
    JobSpecification,
    NotebookSpecification,
    TensorboardSpecification
)
from polyaxon_schemas.utils import TaskType


class TestSpecifications(TestCase):
    def test_notebook_specification_raises_for_invalid_run_section(self):
        with self.assertRaises(PolyaxonfileError):
            NotebookSpecification.read({'version': 1, 'kind': 'notebook'})

        with self.assertRaises(PolyaxonfileError):
            NotebookSpecification.read(os.path.abspath(
                'tests/fixtures/notebook_run_exec_simple_file_with_cmd.yml'))

    def test_tensorboard_specification_raises_for_invalid_run_section(self):
        with self.assertRaises(PolyaxonfileError):
            TensorboardSpecification.read({'version': 1, 'kind': 'tensorboard'})

        with self.assertRaises(PolyaxonConfigurationError):
            TensorboardSpecification.read(os.path.abspath(
                'tests/fixtures/tensorboard_run_exec_simple_file_with_cmd.yml'))

    def test_job_specification_raises_for_missing_build_section(self):
        with self.assertRaises(PolyaxonfileError):
            JobSpecification.read(os.path.abspath(
                'tests/fixtures/job_missing_build.yml'))

    def test_job_specification_raises_for_missing_run_section(self):
        with self.assertRaises(PolyaxonfileError):
            JobSpecification.read(os.path.abspath(
                'tests/fixtures/job_missing_run_exec.yml'))

    def test_create_notebook_specification(self):
        build_config = {'image': 'blabla'}
        config = NotebookSpecification.create_specification(build_config)
        assert NotebookSpecification.read(config).parsed_data == config
        assert config['build'] == build_config
        spec = NotebookSpecification.create_specification(build_config, to_dict=False)
        assert spec.build.image == build_config['image']

    def test_create_tensorboard_specification(self):
        build_config = {'image': 'blabla'}
        config = TensorboardSpecification.create_specification(build_config)
        assert TensorboardSpecification.read(config).parsed_data == config
        assert config['build'] == build_config
        spec = TensorboardSpecification.create_specification(build_config, to_dict=False)
        assert spec.build.image == build_config['image']

    def test_create_build_specification(self):
        # Normal build config
        build_config = {'image': 'blabla'}
        config = BuildSpecification.create_specification(build_config)
        assert BuildSpecification.read(config).parsed_data == config
        assert config['build'] == build_config
        spec = BuildSpecification.create_specification(build_config, to_dict=False)
        assert spec.build.image == build_config['image']

        # Run config
        run_config = {'image': 'blabla', 'cmd': 'some command'}
        config = BuildSpecification.create_specification(run_config)
        assert BuildSpecification.read(config).parsed_data == config
        assert config['build'] == {'image': 'blabla'}
        spec = BuildSpecification.create_specification(run_config, to_dict=False)
        assert spec.build.image == run_config['image']

    def test_create_job_specification(self):
        build_config = {'image': 'blabla'}
        run_config = {'cmd': 'some command'}
        config = JobSpecification.create_specification(build_config=build_config,
                                                       run_config=run_config)
        assert JobSpecification.read(config).parsed_data == config
        assert config['run'] == run_config
        assert config['build'] == build_config
        spec = JobSpecification.create_specification(build_config=build_config,
                                                     run_config=run_config,
                                                     to_dict=False)
        assert spec.build.image == build_config['image']
        assert spec.run.cmd == run_config['cmd']

    def test_cluster_def_without_framework(self):
        spec = ExperimentSpecification.read(os.path.abspath(
            'tests/fixtures/env_without_framework.yml'))
        self.assertEqual(spec.cluster_def, ({TaskType.MASTER: 1}, False))

    def test_patch(self):
        content = {
            'version': 1,
            'kind': 'experiment',
            'build': {'image': 'my_image'},
            'run': {'cmd': 'train'}
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
        matrix = {'hptuning': {'matrix': {'lr': {'values': [0.1, 0.2]}}}}
        with self.assertRaises(PolyaxonfileError):
            spec.patch(values=matrix)

        # Patch with unsupported spec
        wrong_config = {'lr': {'values': [0.1, 0.2]}}
        with self.assertRaises(PolyaxonfileError):
            spec.patch(values=wrong_config)
