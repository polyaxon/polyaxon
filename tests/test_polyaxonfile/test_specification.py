# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

from flaky import flaky
from marshmallow import ValidationError
from tests.utils import assert_equal_dict

from polyaxon_schemas.exceptions import PolyaxonConfigurationError, PolyaxonfileError
from polyaxon_schemas.ops.environments.resources import K8SResourcesConfig, PodResourcesConfig
from polyaxon_schemas.ops.experiment import ExperimentConfig
from polyaxon_schemas.ops.experiment.environment import ExperimentEnvironmentConfig
from polyaxon_schemas.specs import (
    BuildSpecification,
    ExperimentSpecification,
    GroupSpecification,
    JobSpecification,
    NotebookSpecification,
    TensorboardSpecification
)
from polyaxon_schemas.utils import TaskType


class TestSpecifications(TestCase):
    def test_non_yaml_spec(self):
        config = ',sdf;ldjks'
        with self.assertRaises(PolyaxonConfigurationError):
            BuildSpecification.read(config)

        with self.assertRaises(PolyaxonConfigurationError):
            JobSpecification.read(config)

        with self.assertRaises(PolyaxonConfigurationError):
            ExperimentSpecification.read(config)

        with self.assertRaises(PolyaxonConfigurationError):
            GroupSpecification.read(config)

        with self.assertRaises(PolyaxonConfigurationError):
            NotebookSpecification.read(config)

        with self.assertRaises(PolyaxonConfigurationError):
            TensorboardSpecification.read(config)

    def test_notebook_specification_raises_for_invalid_run_section(self):
        with self.assertRaises(PolyaxonfileError):
            NotebookSpecification.read({'version': 1, 'kind': 'notebook'})

        with self.assertRaises(PolyaxonfileError):
            NotebookSpecification.read(os.path.abspath(
                'tests/fixtures/plain/notebook_run_cmd_simple_file_with_cmd.yml'))

    def test_tensorboard_specification_raises_for_invalid_run_section(self):
        with self.assertRaises(PolyaxonfileError):
            TensorboardSpecification.read({'version': 1, 'kind': 'tensorboard'})

        with self.assertRaises(PolyaxonConfigurationError):
            TensorboardSpecification.read(os.path.abspath(
                'tests/fixtures/plain/tensorboard_run_cmd_simple_file_with_cmd.yml'))

    def test_job_specification_raises_for_missing_build_section(self):
        with self.assertRaises(PolyaxonfileError):
            JobSpecification.read(os.path.abspath(
                'tests/fixtures/plain/job_missing_build.yml'))

    def test_job_specification_raises_for_missing_run_section(self):
        with self.assertRaises(PolyaxonfileError):
            JobSpecification.read(os.path.abspath(
                'tests/fixtures/plain/job_missing_run_cmd.yml'))

    def test_create_notebook_specification(self):
        build_config = {'image': 'blabla'}
        config = NotebookSpecification.create_specification(build_config)
        spec = NotebookSpecification.read(config)
        spec.apply_context()
        assert spec.parsed_data == config
        spec = NotebookSpecification.read(spec.raw_data)
        spec.apply_context()
        assert spec.parsed_data == config
        assert config['build'] == build_config
        spec = NotebookSpecification.create_specification(build_config, to_dict=False)
        spec.apply_context()
        assert spec.build.image == build_config['image']

    def test_create_tensorboard_specification(self):
        build_config = {'image': 'blabla'}
        config = TensorboardSpecification.create_specification(build_config)
        spec = TensorboardSpecification.read(config)
        spec.apply_context()
        assert spec.parsed_data == config
        new_spec = TensorboardSpecification.read(spec.raw_data)
        new_spec.apply_context()
        assert new_spec.parsed_data == config
        assert config['build'] == build_config
        spec = TensorboardSpecification.create_specification(build_config, to_dict=False)
        spec.apply_context()
        assert spec.build.image == build_config['image']

    def test_create_build_specification(self):
        # Normal build config
        build_config = {'image': 'blabla'}
        config = BuildSpecification.create_specification(build_config)
        spec = BuildSpecification.read(config)
        spec.apply_context()
        assert spec.parsed_data == config
        new_spec = BuildSpecification.read(spec.raw_data)
        new_spec.apply_context()
        assert new_spec.parsed_data == config
        assert config['image'] == build_config['image']
        spec = BuildSpecification.create_specification(build_config, to_dict=False)
        spec.apply_context()
        assert spec.config.image == build_config['image']

        # Run config
        run_config = {'image': 'blabla', 'cmd': 'some command'}
        config = BuildSpecification.create_specification(run_config)
        spec = BuildSpecification.read(config)
        spec.apply_context()
        assert spec.parsed_data == config

        config = BuildSpecification.create_specification(run_config,
                                                         config_map_refs=None,
                                                         secret_refs=None)
        assert 'config_map_refs' not in config
        assert 'secret_refs' not in config

        config = BuildSpecification.create_specification(run_config, config_map_refs=['foo'])
        spec = BuildSpecification.read(config)
        spec.apply_context()
        assert spec.parsed_data == config
        assert config['environment']['config_map_refs'] == ['foo']
        config = BuildSpecification.create_specification(run_config, secret_refs=['foo'])
        spec = BuildSpecification.read(config)
        spec.apply_context()
        assert spec.parsed_data == config
        assert config['environment']['secret_refs'] == ['foo']

        assert config['image'] == 'blabla'
        spec = BuildSpecification.create_specification(run_config, to_dict=False)
        spec.apply_context()
        assert spec.config.image == run_config['image']

        assert config['image'] == 'blabla'
        spec = BuildSpecification.create_specification(run_config,
                                                       config_map_refs=['foo'],
                                                       secret_refs=['foo'],
                                                       to_dict=False)
        spec.apply_context()
        assert spec.config.image == run_config['image']
        assert spec.environment.secret_refs == ['foo']
        assert spec.environment.config_map_refs == ['foo']

    def test_create_job_specification(self):
        build_config = {'image': 'blabla'}
        run_config = {'cmd': 'some command'}
        config = JobSpecification.create_specification(build_config=build_config,
                                                       run_config=run_config)
        spec = JobSpecification.read(config)
        spec.apply_context()
        spec = JobSpecification.read(spec.raw_data)
        spec.apply_context()
        assert spec.parsed_data == config
        spec = JobSpecification.read(config)
        spec.apply_context()
        assert spec.parsed_data == config
        assert config['run'] == run_config
        assert config['build'] == build_config
        spec = JobSpecification.create_specification(build_config=build_config,
                                                     run_config=run_config,
                                                     to_dict=False)
        spec.apply_context()
        assert spec.build.image == build_config['image']
        assert spec.run.cmd == run_config['cmd']

    def test_cluster_def_without_framework(self):
        spec = ExperimentSpecification.read(os.path.abspath(
            'tests/fixtures/plain/env_without_framework.yml'))
        spec.apply_context()
        self.assertEqual(spec.cluster_def, ({TaskType.MASTER: 1}, False))

    def test_patch_experiment(self):
        content = {
            'version': 1,
            'kind': 'experiment',
            'build': {'image': 'my_image'},
            'run': {'cmd': 'train'}
        }
        spec = ExperimentSpecification.read(content)
        spec.apply_context()
        new_spec = ExperimentSpecification.read(spec.raw_data)
        new_spec.apply_context()
        assert new_spec.parsed_data == content
        assert spec.params is None

        # Add params
        params = {'params': {'lr': 0.1}}
        spec = spec.patch(values=params)
        assert spec.params == params['params']

        # Update params
        params = {'params': {'lr': 0.01, 'num_steps': 100}}
        spec = spec.patch(values=params)
        assert spec.params == params['params']

        # Add env
        assert spec.environment is None
        env = {'environment': {'resources': {
            'gpu': {'requests': 1, 'limits': 1},
            'tpu': {'requests': 1, 'limits': 1}}}}
        spec = spec.patch(values=env)
        assert spec.params == params['params']
        assert spec.environment.resources.gpu.to_dict() == env['environment']['resources']['gpu']
        assert spec.environment.resources.tpu.to_dict() == env['environment']['resources']['gpu']

        # Patch with unsupported spec
        matrix = {'hptuning': {'matrix': {'lr': {'values': [0.1, 0.2]}}}}
        with self.assertRaises(PolyaxonfileError):
            spec.patch(values=matrix)

        # Patch with unsupported spec
        wrong_config = {'lr': {'values': [0.1, 0.2]}}
        with self.assertRaises(PolyaxonfileError):
            spec.patch(values=wrong_config)

    def test_experiment_environment_config(self):
        config_dict = {
            'resources': PodResourcesConfig(cpu=K8SResourcesConfig(0.5, 1)).to_dict(),
            'replicas': {
                'n_workers': 10,
                'n_ps': 5,
            }
        }
        config = ExperimentEnvironmentConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        # Add some field should raise
        config_dict['foo'] = {
            'n_workers': 10,
            'n_ps': 5,
        }

        with self.assertRaises(ValidationError):
            ExperimentEnvironmentConfig.from_dict(config_dict)

        del config_dict['foo']

        experiment_config = {
            'environment': config_dict,
            'framework': 'tensorflow'
        }
        config = ExperimentConfig.from_dict(experiment_config)
        assert_equal_dict(experiment_config, config.to_dict())

        # Removing framework tensorflow should raise
        del experiment_config['framework']
        with self.assertRaises(ValidationError):
            ExperimentConfig.from_dict(experiment_config)

        # Using unknown framework should raise
        experiment_config['framework'] = 'foo'
        with self.assertRaises(ValidationError):
            ExperimentConfig.from_dict(experiment_config)

        # Using known framework
        experiment_config['framework'] = 'mxnet'
        config = ExperimentConfig.from_dict(experiment_config)
        assert_equal_dict(experiment_config, config.to_dict())

        # Adding horovod should raise
        experiment_config['framework'] = 'horovod'
        with self.assertRaises(ValidationError):
            ExperimentConfig.from_dict(experiment_config)

        # Setting correct horovod replicas should pass
        experiment_config['environment']['replicas'] = {
            'n_workers': 5
        }
        config = ExperimentConfig.from_dict(experiment_config)
        assert_equal_dict(experiment_config, config.to_dict())

        # Adding pytorch should pass
        experiment_config['framework'] = 'pytorch'
        config = ExperimentConfig.from_dict(experiment_config)
        assert_equal_dict(experiment_config, config.to_dict())

        # Setting wrong pytorch replicas should raise
        experiment_config['environment']['replicas'] = {
            'n_workers': 5,
            'n_ps': 1
        }

        with self.assertRaises(ValidationError):
            ExperimentConfig.from_dict(experiment_config)

    @flaky(max_runs=3)
    def test_group_environment(self):
        content = {
            'version': 1,
            'kind': 'group',
            'hptuning': {'matrix': {'lr': {'values': [0.1, 0.2]}}},
            'build': {'image': 'my_image'},
            'run': {'cmd': 'train'}
        }
        spec = GroupSpecification.read(content)
        assert GroupSpecification.read(spec.raw_data).raw_data == spec.raw_data
        assert spec.environment is None
        assert spec.config_map_refs is None
        assert spec.secret_refs is None

        content['environment'] = {'config_map_refs': ['foo', 'boo']}
        spec = GroupSpecification.read(content)
        assert spec.environment is not None
        assert spec.config_map_refs == ['foo', 'boo']
        assert spec.secret_refs is None

        content['environment'] = {'secret_refs': ['foo', 'boo']}
        spec = GroupSpecification.read(content)
        assert spec.environment is not None
        assert spec.config_map_refs is None
        assert spec.secret_refs == ['foo', 'boo']

        content['environment'] = {'secret_refs': ['foo', 'boo'], 'config_map_refs': ['foo', 'boo']}
        spec = GroupSpecification.read(content)
        assert spec.environment is not None
        assert spec.config_map_refs == ['foo', 'boo']
        assert spec.secret_refs == ['foo', 'boo']
