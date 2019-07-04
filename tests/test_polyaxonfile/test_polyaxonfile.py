# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

from flaky import flaky

from polyaxon_schemas.exceptions import PolyaxonfileError
from polyaxon_schemas.ops.build_job import BuildConfig
from polyaxon_schemas.ops.environments.pods import EnvironmentConfig
from polyaxon_schemas.ops.environments.resources import K8SResourcesConfig, PodResourcesConfig
from polyaxon_schemas.ops.experiment.backends import ExperimentBackend
from polyaxon_schemas.ops.experiment.frameworks import ExperimentFramework
from polyaxon_schemas.ops.group.early_stopping_policies import EarlyStoppingConfig
from polyaxon_schemas.ops.group.hptuning import HPTuningConfig, SearchAlgorithms
from polyaxon_schemas.ops.group.matrix import MatrixConfig
from polyaxon_schemas.ops.logging import LoggingConfig
from polyaxon_schemas.ops.run import RunConfig
from polyaxon_schemas.polyaxonfile import PolyaxonFile
from polyaxon_schemas.specs.frameworks import (
    HorovodSpecification,
    MPISpecification,
    MXNetSpecification,
    PytorchSpecification,
    TensorflowSpecification
)
from polyaxon_schemas.utils import TaskType


class TestPolyaxonfile(TestCase):
    def test_missing_version_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/plain/missing_version.yml'))

    def test_non_supported_version_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath(
                'tests/fixtures/plain/non_supported_file.yml.yml'))

    def test_missing_kind_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/plain/missing_kind.yml'))

    def test_simple_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/plain/simple_file.yml'), )
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.logging is None
        assert spec.tags is None
        assert spec.params is None
        assert spec.build.image == 'my_image'
        assert spec.run.cmd == 'video_prediction_train --model=DNA --num_masks=1'
        assert spec.environment is None
        assert spec.framework is None
        assert spec.is_experiment
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.is_experiment is True

    def test_passing_params_overrides_polyaxon_files(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/plain/simple_file.yml'),
                               params={'foo': 'bar', 'value': 1.1})
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.logging is None
        assert spec.tags is None
        assert spec.params == {'foo': 'bar', 'value': 1.1}
        assert spec.build.image == 'my_image'
        assert spec.run.cmd == 'video_prediction_train --model=DNA --num_masks=1'
        assert spec.environment is None
        assert spec.framework is None
        assert spec.is_experiment
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.is_experiment is True

    def test_passing_wrong_params_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/plain/simple_file.yml'), params='foo')

    def test_simple_file_framework_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/plain/simple_file_framework.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.logging is None
        assert spec.tags is None
        assert spec.build.dockerfile == 'Dockerfile'
        assert spec.run.cmd == 'video_prediction_train --model=DNA --num_masks=1'
        assert spec.environment is not None
        assert spec.environment.resources.gpu.to_dict() == {'requests': 1, 'limits': 1}
        assert spec.framework is not None
        assert spec.is_experiment is True

    def test_advanced_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/plain/advanced_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert isinstance(spec.logging, LoggingConfig)
        assert spec.is_experiment
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.framework == ExperimentFramework.TENSORFLOW
        assert spec.config.tensorflow.n_workers == 5
        assert spec.config.tensorflow.n_ps == 10

        # check properties for returning worker configs and resources
        assert spec.config.tensorflow.worker_resources == {}
        assert spec.config.tensorflow.ps_resources == {}

        cluster, is_distributed = spec.cluster_def

        assert TensorflowSpecification.get_worker_resources(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        ) == {}
        assert TensorflowSpecification.get_ps_resources(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        ) == {}

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.PS: 10}, True)

    def test_advanced_file_with_custom_configs_and_resources_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/advanced_file_with_custom_configs_and_resources.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert isinstance(spec.logging, LoggingConfig)
        assert spec.is_experiment
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.framework == ExperimentFramework.TENSORFLOW
        assert spec.artifact_refs == ['outputs1']
        assert spec.data_refs == ['data1', 'data2']
        assert spec.secret_refs == ['secret1', 'secret2']
        assert spec.config_map_refs == ['config_map1', 'config_map2']
        assert spec.config.tensorflow.n_workers == 5
        assert spec.config.tensorflow.n_ps == 10

        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert spec.config.tensorflow.default_worker_node_selector == {
            'foo': True
        }

        assert spec.config.tensorflow.worker_resources == {}
        assert spec.config.tensorflow.worker_affinities == {}
        assert isinstance(spec.config.tensorflow.worker_node_selectors[3], dict)
        assert spec.config.tensorflow.worker_node_selectors[3] == {
            'foo': False
        }
        assert isinstance(spec.config.tensorflow.worker_tolerations[4], list)
        assert spec.config.tensorflow.worker_tolerations[4] == [{
            'key': 'key',
            'operator': 'Exists',
            'effect': 'NoSchedule',
        }]

        assert isinstance(spec.config.tensorflow.default_ps_resources, PodResourcesConfig)
        assert isinstance(spec.config.tensorflow.default_ps_resources.cpu, K8SResourcesConfig)
        assert spec.config.tensorflow.default_ps_resources.cpu.requests == 2
        assert spec.config.tensorflow.default_ps_resources.cpu.limits == 4

        assert spec.config.tensorflow.ps_node_selectors == {}
        assert isinstance(spec.config.tensorflow.ps_tolerations[7], list)
        assert spec.config.tensorflow.ps_tolerations[7] == [{
            'operator': 'Exists'
        }]
        assert isinstance(spec.config.tensorflow.ps_affinities[7], dict)
        assert isinstance(spec.config.tensorflow.ps_resources[9], PodResourcesConfig)
        assert isinstance(spec.config.tensorflow.ps_resources[9].memory, K8SResourcesConfig)
        assert spec.config.tensorflow.ps_resources[9].memory.requests == 512
        assert spec.config.tensorflow.ps_resources[9].memory.limits == 1024

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_node_selectors = TensorflowSpecification.get_worker_node_selectors(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_node_selectors) == spec.config.tensorflow.n_workers
        assert set([i['foo'] for i in worker_node_selectors.values()]) == {
            spec.config.tensorflow.default_worker_node_selector['foo'],
            spec.config.tensorflow.worker_node_selectors[3]['foo']}

        assert TensorflowSpecification.get_worker_resources(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        ) == {}
        ps_resources = TensorflowSpecification.get_ps_resources(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_resources) == spec.config.tensorflow.n_ps
        assert set(ps_resources.values()) == {
            spec.config.tensorflow.default_ps_resources,
            spec.config.tensorflow.ps_resources[9]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 2 * 9, 'limits': 2 + 4 * 9},
            'memory': {'requests': 512, 'limits': 1024},
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.PS: 10}, True)

    def test_wrong_grid_matrix_file_passes(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/plain/wrong_grid_matrix_file.yml'))

    @flaky(max_runs=3)
    def test_matrix_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/plain/matrix_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_group
        assert isinstance(spec.hptuning.matrix['lr'], MatrixConfig)
        assert isinstance(spec.hptuning.matrix['loss'], MatrixConfig)
        assert spec.hptuning.matrix['lr'].to_dict() == {
            'linspace': {'start': 0.01, 'stop': 0.1, 'num': 5}}
        assert spec.hptuning.matrix['loss'].to_dict() == {'values': ['MeanSquaredError',
                                                                     'AbsoluteDifference']}
        assert spec.matrix_space == 10
        assert isinstance(spec.hptuning, HPTuningConfig)
        assert spec.hptuning.concurrency == 2
        assert spec.search_algorithm == SearchAlgorithms.GRID
        assert spec.hptuning.early_stopping is None
        assert spec.early_stopping == []

        assert spec.experiments_def == {
            'search_algorithm': SearchAlgorithms.GRID,
            'early_stopping': False,
            'concurrency': 2,
        }

        build = spec.build
        assert build is None

        spec = spec.get_experiment_spec(matrix_declaration=spec.matrix_declaration_test)
        spec.apply_context()
        assert spec.environment is not None
        assert spec.artifact_refs == ['outputs1']
        assert spec.data_refs == ['data1', 'data2']
        # TODO
        # assert spec.outputs.jobs == [111]
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.run.cmd == 'train --lr={lr} --loss={loss}'.format(
            **spec.params
        )

    def test_matrix_file_passes_int_float_types(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/matrix_file_with_int_float_types.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_group
        assert isinstance(spec.hptuning.matrix['param1'], MatrixConfig)
        assert isinstance(spec.hptuning.matrix['param2'], MatrixConfig)
        assert spec.hptuning.matrix['param1'].to_dict() == {'values': [1, 2]}
        assert spec.hptuning.matrix['param2'].to_dict() == {'values': [3.3, 4.4]}
        assert spec.matrix_space == 4
        assert isinstance(spec.hptuning, HPTuningConfig)
        assert spec.hptuning.concurrency == 2
        assert spec.search_algorithm == SearchAlgorithms.GRID
        assert spec.hptuning.early_stopping is None
        assert spec.early_stopping == []

        assert spec.experiments_def == {
            'search_algorithm': SearchAlgorithms.GRID,
            'early_stopping': False,
            'concurrency': 2,
        }

        build = spec.build
        assert build is None

        spec = spec.get_experiment_spec(matrix_declaration=spec.matrix_declaration_test)
        spec.apply_context()
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.run.cmd == 'train --param1={param1} --param2={param2}'.format(
            **spec.params
        )

    @flaky(max_runs=3)
    def test_matrix_early_stopping_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/matrix_file_early_stopping.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_group
        assert isinstance(spec.hptuning.matrix['lr'], MatrixConfig)
        assert isinstance(spec.hptuning.matrix['loss'], MatrixConfig)
        assert spec.hptuning.matrix['lr'].to_dict() == {
            'linspace': {'start': 0.01, 'stop': 0.1, 'num': 5}}
        assert spec.hptuning.matrix['loss'].to_dict() == {'values': ['MeanSquaredError',
                                                                     'AbsoluteDifference']}
        assert spec.matrix_space == 10
        assert isinstance(spec.hptuning, HPTuningConfig)
        assert spec.hptuning.concurrency == 2
        assert spec.hptuning.random_search.n_experiments == 5
        assert spec.early_stopping == spec.hptuning.early_stopping
        assert len(spec.hptuning.early_stopping) == 1
        assert isinstance(spec.hptuning.early_stopping[0], EarlyStoppingConfig)

        assert spec.experiments_def == {
            'search_algorithm': SearchAlgorithms.RANDOM,
            'early_stopping': True,
            'concurrency': 2,
            'n_experiments': 5
        }

        build = spec.build
        assert build is None

        spec = spec.get_experiment_spec(matrix_declaration=spec.matrix_declaration_test)
        spec.apply_context()
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.run.cmd == 'train --lr={lr} --loss={loss}'.format(
            **spec.params
        )

    @flaky(max_runs=3)
    def test_matrix_large_n_experiments_ignored_file_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath('tests/fixtures/plain/matrix_file_ignored_n_experiments.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_group
        assert isinstance(spec.hptuning.matrix['lr'], MatrixConfig)
        assert isinstance(spec.hptuning.matrix['loss'], MatrixConfig)
        assert spec.hptuning.matrix['lr'].to_dict() == {
            'linspace': {'start': 0.01, 'stop': 0.1, 'num': 5}}
        assert spec.hptuning.matrix['loss'].to_dict() == {'values': ['MeanSquaredError',
                                                                     'AbsoluteDifference']}
        assert spec.matrix_space == 10
        assert isinstance(spec.hptuning, HPTuningConfig)
        assert spec.hptuning.concurrency == 2
        assert spec.search_algorithm == SearchAlgorithms.RANDOM
        assert spec.hptuning.random_search.n_experiments == 300
        assert spec.early_stopping == []

        assert spec.experiments_def == {
            'search_algorithm': SearchAlgorithms.RANDOM,
            'early_stopping': False,
            'concurrency': 2,
            'n_experiments': 300
        }

        build = spec.build
        assert build is None

        spec = spec.get_experiment_spec(matrix_declaration=spec.matrix_declaration_test)
        spec.apply_context()
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.run.cmd == 'train --lr={lr} --loss={loss}'.format(
            **spec.params
        )

    @flaky(max_runs=3)
    def test_one_matrix_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/plain/one_matrix_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_group
        assert spec.hptuning is not None
        assert isinstance(spec.hptuning.matrix['loss'], MatrixConfig)
        assert spec.hptuning.matrix['loss'].to_dict() == {'values': ['MeanSquaredError',
                                                                     'AbsoluteDifference']}
        assert spec.matrix_space == 2

        assert spec.build.ref == 1

        spec = spec.get_experiment_spec(matrix_declaration=spec.matrix_declaration_test)
        spec.apply_context()
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.run.cmd == 'train --loss="{}"'.format(spec.params['loss'])

    def test_run_simple_file_passes_sdf(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/run_cmd_simple_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.logging is None
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert spec.is_experiment
        assert isinstance(spec.build, BuildConfig)
        assert isinstance(spec.run, RunConfig)
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        run = spec.run
        assert isinstance(run, RunConfig)
        assert run.cmd == "video_prediction_train --num_masks=2"

    def test_run_simple_file_with_cmds_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/run_cmd_simple_file_list_cmds.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.logging is None
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert spec.is_experiment
        assert isinstance(spec.build, BuildConfig)
        assert isinstance(spec.run, RunConfig)
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        run = spec.run
        assert isinstance(run, RunConfig)
        assert run.cmd == ['video_prediction_train --model=DNA --num_masks=1',
                           'video_prediction_train --model=DNA --num_masks=10']

    def test_run_simple_file_with_build_env_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/plain/run_cmd_with_build_env.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.logging is None
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert spec.is_experiment
        assert isinstance(spec.build, BuildConfig)
        assert spec.build.environment is not None
        assert spec.build.environment.node_selector == {'polyaxon.com': 'node_for_build_jobs'}
        assert isinstance(spec.build.environment.resources, PodResourcesConfig)
        assert isinstance(spec.build.environment.affinity, dict)
        assert isinstance(spec.run, RunConfig)
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        run = spec.run
        assert isinstance(run, RunConfig)
        assert run.cmd == ['video_prediction_train --model=DNA --num_masks=1',
                           'video_prediction_train --model=DNA --num_masks=10']

    def test_run_matrix_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/plain/run_cmd_matrix_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_group
        assert isinstance(spec.hptuning.matrix['model'], MatrixConfig)
        assert spec.hptuning.matrix['model'].to_dict() == {'values': ['CDNA', 'DNA', 'STP']}
        assert spec.matrix_space == 3
        assert isinstance(spec.hptuning, HPTuningConfig)
        params = spec.matrix_declaration_test

        build = spec.build
        assert isinstance(build, BuildConfig)
        assert build.image == 'my_image'

        spec = spec.get_experiment_spec(params)
        spec.apply_context()
        assert spec.environment is None
        assert spec.logging is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        run = spec.run
        assert isinstance(run, RunConfig)
        # params['num_masks'] = 1 if params['model'] == 'DNA' else 10
        params['num_masks'] = 10
        assert run.cmd == ('video_prediction_train '
                           '--model="{model}" '
                           '--num_masks={num_masks}').format(
            **params
        )

    def test_run_matrix_sampling_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/run_cmd_matrix_sampling_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_group
        assert isinstance(spec.build, BuildConfig)
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert isinstance(spec.hptuning.matrix['model'], MatrixConfig)
        assert spec.hptuning.matrix['learning_rate'].to_dict() == {
            'normal': {'loc': 0, 'scale': 0.9}}
        assert spec.hptuning.matrix['dropout'].to_dict() == {
            'qloguniform': {'high': 0.8, 'low': 0, 'q': 0.1}}
        assert spec.hptuning.matrix['activation'].to_dict() == {
            'pvalues': [['relu', 0.1], ['sigmoid', 0.8]]}
        assert spec.hptuning.matrix['model'].to_dict() == {'values': ['CDNA', 'DNA', 'STP']}
        assert isinstance(spec.hptuning, HPTuningConfig)
        params = spec.matrix_declaration_test

        build = spec.build
        assert isinstance(build, BuildConfig)
        assert build.image == 'my_image'

        spec = spec.get_experiment_spec(params)
        spec.apply_context()
        assert spec.environment is None
        assert spec.logging is not None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        run = spec.run
        assert isinstance(run, RunConfig)
        # params['num_masks'] = 1 if params['model'] == 'DNA' else 10
        params['num_masks'] = 10
        assert run.cmd == ('video_prediction_train '
                           '--model="{model}" '
                           '--num_masks={num_masks}').format(
            **params
        )

    def test_distributed_tensorflow_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/distributed_tensorflow_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert isinstance(spec.logging, LoggingConfig)
        assert spec.is_experiment
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.environment.node_selector is None
        assert spec.master_node_selector is None
        assert spec.framework == ExperimentFramework.TENSORFLOW
        assert spec.config.tensorflow.n_workers == 5
        assert spec.config.tensorflow.n_ps == 10

        assert spec.environment.tolerations is None
        assert spec.environment.node_selector is None
        assert isinstance(spec.environment.affinity, dict)
        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert spec.config.tensorflow.default_worker_node_selector is None
        assert spec.config.tensorflow.default_worker_affinity is None
        assert isinstance(spec.config.tensorflow.default_worker_tolerations, list)
        assert isinstance(spec.config.tensorflow.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.config.tensorflow.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.config.tensorflow.default_worker_resources.cpu.requests == 3
        assert spec.config.tensorflow.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.config.tensorflow.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.config.tensorflow.default_worker_resources.memory.requests == 256
        assert spec.config.tensorflow.default_worker_resources.memory.limits == 256

        assert spec.config.tensorflow.worker_tolerations[2] == [{'operator': 'Exists'}]
        assert isinstance(spec.config.tensorflow.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.config.tensorflow.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.config.tensorflow.worker_resources[3].memory.requests == 300
        assert spec.config.tensorflow.worker_resources[3].memory.limits == 300

        assert spec.config.tensorflow.default_ps_node_selector is None
        assert spec.config.tensorflow.default_ps_affinity is None
        assert isinstance(spec.config.tensorflow.default_ps_tolerations, list)
        assert isinstance(spec.config.tensorflow.default_ps_resources, PodResourcesConfig)
        assert isinstance(spec.config.tensorflow.default_ps_resources.cpu, K8SResourcesConfig)
        assert spec.config.tensorflow.default_ps_resources.cpu.requests == 2
        assert spec.config.tensorflow.default_ps_resources.cpu.limits == 4

        assert isinstance(spec.config.tensorflow.ps_resources[9], PodResourcesConfig)
        assert isinstance(spec.config.tensorflow.ps_resources[9].memory, K8SResourcesConfig)
        assert spec.config.tensorflow.ps_resources[9].memory.requests == 512
        assert spec.config.tensorflow.ps_resources[9].memory.limits == 1024

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_affinities = TensorflowSpecification.get_worker_affinities(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_tolerations = TensorflowSpecification.get_worker_tolerations(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_node_selectors = TensorflowSpecification.get_worker_node_selectors(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_resources = TensorflowSpecification.get_worker_resources(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert worker_affinities == {}
        assert worker_node_selectors == {}
        assert len(worker_tolerations) == spec.config.tensorflow.n_workers
        assert len(worker_resources) == spec.config.tensorflow.n_workers
        assert set(worker_resources.values()) == {
            spec.config.tensorflow.default_worker_resources,
            spec.config.tensorflow.worker_resources[3]}

        ps_tolerations = TensorflowSpecification.get_ps_tolerations(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_affinities = TensorflowSpecification.get_ps_affinities(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_node_selectors = TensorflowSpecification.get_ps_node_selectors(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_resources = TensorflowSpecification.get_ps_resources(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert ps_affinities == {}
        assert ps_node_selectors == {}
        assert len(ps_tolerations) == spec.config.tensorflow.n_ps
        assert len(ps_resources) == spec.config.tensorflow.n_ps
        assert set(ps_resources.values()) == {
            spec.config.tensorflow.default_ps_resources,
            spec.config.tensorflow.ps_resources[9]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4 + 2 * 9, 'limits': 2 + 3 * 4 + 4 * 9},
            'memory': {'requests': 300 + 256 * 4 + 512, 'limits': 300 + 256 * 4 + 1024},
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.PS: 10}, True)

    def test_distributed_tensorflow_passes_with_node_selectors(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/distributed_tensorflow_with_node_selectors_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_experiment
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.environment.node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.master_node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.framework == ExperimentFramework.TENSORFLOW
        assert spec.config.tensorflow.n_workers == 5
        assert spec.config.tensorflow.n_ps == 10

        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert isinstance(spec.config.tensorflow.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.config.tensorflow.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.config.tensorflow.default_worker_resources.cpu.requests == 3
        assert spec.config.tensorflow.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.config.tensorflow.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.config.tensorflow.default_worker_resources.memory.requests == 256
        assert spec.config.tensorflow.default_worker_resources.memory.limits == 256

        assert isinstance(spec.config.tensorflow.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.config.tensorflow.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.config.tensorflow.worker_resources[3].memory.requests == 300
        assert spec.config.tensorflow.worker_resources[3].memory.limits == 300

        assert isinstance(spec.config.tensorflow.default_ps_resources, PodResourcesConfig)
        assert isinstance(spec.config.tensorflow.default_ps_resources.cpu, K8SResourcesConfig)
        assert spec.config.tensorflow.default_ps_resources.cpu.requests == 2
        assert spec.config.tensorflow.default_ps_resources.cpu.limits == 4

        assert isinstance(spec.config.tensorflow.ps_resources[9], PodResourcesConfig)
        assert isinstance(spec.config.tensorflow.ps_resources[9].memory, K8SResourcesConfig)
        assert spec.config.tensorflow.ps_resources[9].memory.requests == 512
        assert spec.config.tensorflow.ps_resources[9].memory.limits == 1024

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = TensorflowSpecification.get_worker_resources(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_resources) == spec.config.tensorflow.n_workers
        assert set(worker_resources.values()) == {
            spec.config.tensorflow.default_worker_resources,
            spec.config.tensorflow.worker_resources[3]}

        ps_resources = TensorflowSpecification.get_ps_resources(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_resources) == spec.config.tensorflow.n_ps
        assert set(ps_resources.values()) == {
            spec.config.tensorflow.default_ps_resources,
            spec.config.tensorflow.ps_resources[9]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4 + 2 * 9, 'limits': 2 + 3 * 4 + 4 * 9},
            'memory': {'requests': 300 + 256 * 4 + 512, 'limits': 300 + 256 * 4 + 1024},
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.PS: 10}, True)

        assert (spec.config.tensorflow.default_worker.node_selector ==
                {'polyaxon.com': 'node_for_worker_tasks'})
        assert (spec.config.tensorflow.worker_node_selectors[2] ==
                {'polyaxon.com': 'node_for_worker_task_2'})

        assert (spec.config.tensorflow.default_ps.node_selector ==
                {'polyaxon.com': 'node_for_ps_tasks'})
        assert (spec.config.tensorflow.ps_node_selectors[2] ==
                {'polyaxon.com': 'node_for_ps_task_2'})

        worker_node_selectors = TensorflowSpecification.get_worker_node_selectors(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_node_selectors) == spec.config.tensorflow.n_workers
        assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
            tuple(spec.config.tensorflow.default_worker.node_selector.items()),
            tuple(spec.config.tensorflow.worker_node_selectors[2].items())}

        ps_node_selectors = TensorflowSpecification.get_ps_node_selectors(
            environment=spec.config.tensorflow,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_node_selectors) == spec.config.tensorflow.n_ps
        assert set(tuple(i.items()) for i in ps_node_selectors.values()) == {
            tuple(spec.config.tensorflow.default_ps.node_selector.items()),
            tuple(spec.config.tensorflow.ps_node_selectors[2].items())}

    def test_distributed_horovod_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/plain/distributed_horovod_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_experiment
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.framework == ExperimentFramework.HOROVOD
        assert spec.config.horovod.n_workers == 5

        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert isinstance(spec.config.horovod.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.config.horovod.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.config.horovod.default_worker_resources.cpu.requests == 3
        assert spec.config.horovod.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.config.horovod.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.config.horovod.default_worker_resources.memory.requests == 256
        assert spec.config.horovod.default_worker_resources.memory.limits == 256

        assert isinstance(spec.config.horovod.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.config.horovod.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.config.horovod.worker_resources[3].memory.requests == 300
        assert spec.config.horovod.worker_resources[3].memory.limits == 300

        assert isinstance(spec.environment.affinity, dict)
        assert spec.config.horovod.worker_affinities == {}

        assert spec.environment.tolerations is None
        assert isinstance(spec.config.horovod.default_worker_tolerations, list)
        assert isinstance(spec.config.horovod.worker_tolerations[2], list)
        assert spec.config.horovod.worker_tolerations[2] == [{'operator': 'Exists'}]

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = HorovodSpecification.get_worker_resources(
            environment=spec.config.horovod,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_node_selectors = HorovodSpecification.get_worker_node_selectors(
            environment=spec.config.horovod,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_affinities = HorovodSpecification.get_worker_affinities(
            environment=spec.config.horovod,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_tolerations = HorovodSpecification.get_worker_tolerations(
            environment=spec.config.horovod,
            cluster=cluster,
            is_distributed=is_distributed
        )

        assert worker_node_selectors == {}
        assert worker_affinities == {}
        assert len(worker_tolerations) == spec.config.horovod.n_workers
        assert len(worker_resources) == spec.config.horovod.n_workers
        assert set(worker_resources.values()) == {
            spec.config.horovod.default_worker_resources,
            spec.config.horovod.worker_resources[3]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4, 'limits': 2 + 3 * 4},
            'memory': {'requests': 300 + 256 * 4, 'limits': 300 + 256 * 4},
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5}, True)

    def test_distributed_horovod_with_node_selectors_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/distributed_horovod_with_node_selectors_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_experiment
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.environment.node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.master_node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.framework == ExperimentFramework.HOROVOD
        assert spec.config.horovod.n_workers == 5

        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert isinstance(spec.config.horovod.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.config.horovod.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.config.horovod.default_worker_resources.cpu.requests == 3
        assert spec.config.horovod.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.config.horovod.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.config.horovod.default_worker_resources.memory.requests == 256
        assert spec.config.horovod.default_worker_resources.memory.limits == 256

        assert isinstance(spec.config.horovod.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.config.horovod.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.config.horovod.worker_resources[3].memory.requests == 300
        assert spec.config.horovod.worker_resources[3].memory.limits == 300

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = HorovodSpecification.get_worker_resources(
            environment=spec.config.horovod,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_resources) == spec.config.horovod.n_workers
        assert set(worker_resources.values()) == {
            spec.config.horovod.default_worker_resources,
            spec.config.horovod.worker_resources[3]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4, 'limits': 2 + 3 * 4},
            'memory': {'requests': 300 + 256 * 4, 'limits': 300 + 256 * 4},
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5}, True)

        assert (spec.config.horovod.default_worker.node_selector ==
                {'polyaxon.com': 'node_for_worker_tasks'})
        assert (spec.config.horovod.worker_node_selectors[2] ==
                {'polyaxon.com': 'node_for_worker_task_2'})

        worker_node_selectors = HorovodSpecification.get_worker_node_selectors(
            environment=spec.config.horovod,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_node_selectors) == spec.config.horovod.n_workers
        assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
            tuple(spec.config.horovod.default_worker.node_selector.items()),
            tuple(spec.config.horovod.worker_node_selectors[2].items())}

    def test_distributed_pytorch_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/distributed_pytorch_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_experiment
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.framework == ExperimentFramework.PYTORCH
        assert spec.config.pytorch.n_workers == 5

        assert spec.environment.node_selector is None
        assert spec.environment.tolerations is None
        assert isinstance(spec.environment.affinity, dict)
        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert spec.config.pytorch.default_worker_node_selector is None
        assert spec.config.pytorch.default_worker_affinity is None
        assert isinstance(spec.config.pytorch.default_worker_tolerations, list)
        assert isinstance(spec.config.pytorch.default_worker_tolerations[0], dict)
        assert isinstance(spec.config.pytorch.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.config.pytorch.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.config.pytorch.default_worker_resources.cpu.requests == 3
        assert spec.config.pytorch.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.config.pytorch.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.config.pytorch.default_worker_resources.memory.requests == 256
        assert spec.config.pytorch.default_worker_resources.memory.limits == 256

        assert spec.config.pytorch.worker_tolerations[2] == [{'operator': 'Exists'}]
        assert isinstance(spec.config.pytorch.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.config.pytorch.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.config.pytorch.worker_resources[3].memory.requests == 300
        assert spec.config.pytorch.worker_resources[3].memory.limits == 300

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = PytorchSpecification.get_worker_resources(
            environment=spec.config.pytorch,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_tolerations = PytorchSpecification.get_worker_tolerations(
            environment=spec.config.pytorch,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_node_selectors = PytorchSpecification.get_worker_node_selectors(
            environment=spec.config.pytorch,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_affinities = PytorchSpecification.get_worker_affinities(
            environment=spec.config.pytorch,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert worker_node_selectors == {}
        assert worker_affinities == {}
        assert len(worker_tolerations) == spec.config.pytorch.n_workers
        assert len(worker_resources) == spec.config.pytorch.n_workers
        assert set(worker_resources.values()) == {
            spec.config.pytorch.default_worker_resources,
            spec.config.pytorch.worker_resources[3]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4, 'limits': 2 + 3 * 4},
            'memory': {'requests': 300 + 256 * 4, 'limits': 300 + 256 * 4},
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5}, True)

    def test_distributed_pytorch_with_node_selectors_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/distributed_pytorch_with_node_selectors_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_experiment
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.environment.node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.master_node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.framework == ExperimentFramework.PYTORCH
        assert spec.config.pytorch.n_workers == 5

        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert isinstance(spec.config.pytorch.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.config.pytorch.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.config.pytorch.default_worker_resources.cpu.requests == 3
        assert spec.config.pytorch.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.config.pytorch.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.config.pytorch.default_worker_resources.memory.requests == 256
        assert spec.config.pytorch.default_worker_resources.memory.limits == 256

        assert isinstance(spec.config.pytorch.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.config.pytorch.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.config.pytorch.worker_resources[3].memory.requests == 300
        assert spec.config.pytorch.worker_resources[3].memory.limits == 300

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = PytorchSpecification.get_worker_resources(
            environment=spec.config.pytorch,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_resources) == spec.config.pytorch.n_workers
        assert set(worker_resources.values()) == {
            spec.config.pytorch.default_worker_resources,
            spec.config.pytorch.worker_resources[3]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4, 'limits': 2 + 3 * 4},
            'memory': {'requests': 300 + 256 * 4, 'limits': 300 + 256 * 4},
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5}, True)

        assert (spec.config.pytorch.default_worker.node_selector ==
                {'polyaxon.com': 'node_for_worker_tasks'})
        assert (spec.config.pytorch.worker_node_selectors[2] ==
                {'polyaxon.com': 'node_for_worker_task_2'})

        worker_node_selectors = PytorchSpecification.get_worker_node_selectors(
            environment=spec.config.pytorch,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_node_selectors) == spec.config.pytorch.n_workers
        assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
            tuple(spec.config.pytorch.default_worker.node_selector.items()),
            tuple(spec.config.pytorch.worker_node_selectors[2].items())}

    def test_distributed_mpi_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/distributed_mpi_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_experiment
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.framework == ExperimentFramework.TENSORFLOW
        assert spec.backend == ExperimentBackend.MPI
        assert spec.config.mpi.n_workers == 8

        assert spec.environment.node_selector is None
        assert spec.environment.tolerations is None
        assert spec.environment.affinity is None
        assert spec.environment.resources is None

        assert spec.config.mpi.default_worker_node_selector is None
        assert spec.config.mpi.default_worker_affinity is None
        assert isinstance(spec.config.mpi.default_worker_tolerations, list)
        assert isinstance(spec.config.mpi.default_worker_tolerations[0], dict)
        assert isinstance(spec.config.mpi.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.config.mpi.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.config.mpi.default_worker_resources.cpu.requests == 3
        assert spec.config.mpi.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.config.mpi.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.config.mpi.default_worker_resources.memory.requests == 256
        assert spec.config.mpi.default_worker_resources.memory.limits == 256
        assert isinstance(spec.config.mpi.default_worker_resources.gpu,
                          K8SResourcesConfig)
        assert spec.config.mpi.default_worker_resources.gpu.requests == 4
        assert spec.config.mpi.default_worker_resources.gpu.limits == 4

        assert spec.config.mpi.worker_tolerations == {}
        assert spec.config.mpi.worker_resources == {}

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = PytorchSpecification.get_worker_resources(
            environment=spec.config.mpi,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_tolerations = PytorchSpecification.get_worker_tolerations(
            environment=spec.config.mpi,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_node_selectors = PytorchSpecification.get_worker_node_selectors(
            environment=spec.config.mpi,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_affinities = PytorchSpecification.get_worker_affinities(
            environment=spec.config.mpi,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert worker_node_selectors == {}
        assert worker_affinities == {}
        assert len(worker_tolerations) == spec.config.mpi.n_workers
        assert len(worker_resources) == spec.config.mpi.n_workers
        assert set(worker_resources.values()) == {spec.config.mpi.default_worker_resources}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 3 * 8, 'limits': 3 * 8},
            'memory': {'requests': 256 * 8, 'limits': 256 * 8},
            'gpu': {'requests': 4 * 8, 'limits': 4 * 8},
        }

        assert spec.cluster_def == ({TaskType.WORKER: 8}, True)

    def test_distributed_mpi_with_node_selectors_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/distributed_mpi_with_node_selectors_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_experiment
        assert spec.framework == ExperimentFramework.PYTORCH
        assert spec.backend == ExperimentBackend.MPI
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.environment.node_selector is None
        assert spec.master_node_selector is None
        assert spec.config.mpi.n_workers == 4

        assert spec.environment.resources is None

        assert isinstance(spec.config.mpi.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.config.mpi.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.config.mpi.default_worker_resources.cpu.requests == 3
        assert spec.config.mpi.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.config.mpi.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.config.mpi.default_worker_resources.memory.requests == 256
        assert spec.config.mpi.default_worker_resources.memory.limits == 256
        assert isinstance(spec.config.mpi.default_worker_resources.gpu,
                          K8SResourcesConfig)
        assert spec.config.mpi.default_worker_resources.gpu.requests == 2
        assert spec.config.mpi.default_worker_resources.gpu.limits == 2

        assert spec.config.mpi.worker_resources == {}

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = PytorchSpecification.get_worker_resources(
            environment=spec.config.mpi,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_resources) == spec.config.mpi.n_workers
        assert set(worker_resources.values()) == {spec.config.mpi.default_worker_resources}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 3 * 4, 'limits': 3 * 4},
            'memory': {'requests': 256 * 4, 'limits': 256 * 4},
            'gpu': {'requests': 4 * 2, 'limits': 4 * 2},
        }

        assert spec.cluster_def == ({TaskType.WORKER: 4}, True)

        assert (spec.config.mpi.default_worker.node_selector ==
                {'polyaxon.com': 'node_for_worker_tasks'})

        worker_node_selectors = MPISpecification.get_worker_node_selectors(
            environment=spec.config.mpi,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_node_selectors) == spec.config.mpi.n_workers
        assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
            tuple(spec.config.mpi.default_worker.node_selector.items())}

    def test_distributed_mxnet_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/distributed_mxnet_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_experiment
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.framework == ExperimentFramework.MXNET
        assert spec.config.mxnet.n_workers == 5
        assert spec.config.mxnet.n_ps == 10

        assert spec.environment.node_selector is None
        assert spec.environment.tolerations is None
        assert isinstance(spec.environment.affinity, dict)
        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert spec.config.mxnet.default_worker_node_selector is None
        assert spec.config.mxnet.default_worker_affinity is None
        assert isinstance(spec.config.mxnet.default_worker_tolerations, list)
        assert isinstance(spec.config.mxnet.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.config.mxnet.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.config.mxnet.default_worker_resources.cpu.requests == 3
        assert spec.config.mxnet.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.config.mxnet.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.config.mxnet.default_worker_resources.memory.requests == 256
        assert spec.config.mxnet.default_worker_resources.memory.limits == 256

        assert isinstance(spec.config.mxnet.worker_tolerations[2], list)
        assert spec.config.mxnet.worker_tolerations[2] == [{'operator': 'Exists'}]
        assert isinstance(spec.config.mxnet.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.config.mxnet.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.config.mxnet.worker_resources[3].memory.requests == 300
        assert spec.config.mxnet.worker_resources[3].memory.limits == 300

        assert spec.config.mxnet.default_ps_node_selector is None
        assert spec.config.mxnet.default_ps_affinity is None
        assert isinstance(spec.config.mxnet.default_ps_tolerations, list)
        assert isinstance(spec.config.mxnet.default_ps_resources,
                          PodResourcesConfig)
        assert isinstance(spec.config.mxnet.default_ps_resources.cpu,
                          K8SResourcesConfig)
        assert spec.config.mxnet.default_ps_resources.cpu.requests == 2
        assert spec.config.mxnet.default_ps_resources.cpu.limits == 4

        assert isinstance(spec.config.mxnet.ps_resources[9],
                          PodResourcesConfig)
        assert isinstance(spec.config.mxnet.ps_resources[9].memory,
                          K8SResourcesConfig)
        assert spec.config.mxnet.ps_resources[9].memory.requests == 512
        assert spec.config.mxnet.ps_resources[9].memory.limits == 1024

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = MXNetSpecification.get_worker_resources(
            environment=spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_node_selectors = MXNetSpecification.get_worker_node_selectors(
            environment=spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_affinities = MXNetSpecification.get_worker_affinities(
            environment=spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_tolerations = MXNetSpecification.get_worker_tolerations(
            environment=spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert worker_node_selectors == {}
        assert worker_affinities == {}
        assert len(worker_tolerations) == spec.config.mxnet.n_workers
        assert len(worker_resources) == spec.config.mxnet.n_workers
        assert set(worker_resources.values()) == {
            spec.config.mxnet.default_worker_resources,
            spec.config.mxnet.worker_resources[3]}

        ps_resources = MXNetSpecification.get_ps_resources(
            environment=spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_node_selectors = MXNetSpecification.get_ps_node_selectors(
            environment=spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_affinities = MXNetSpecification.get_ps_affinities(
            environment=spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_tolerations = MXNetSpecification.get_ps_tolerations(
            environment=spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert ps_node_selectors == {}
        assert ps_affinities == {}
        assert len(ps_tolerations) == spec.config.mxnet.n_ps
        assert len(ps_resources) == spec.config.mxnet.n_ps
        assert set(ps_resources.values()) == {
            spec.config.mxnet.default_ps_resources,
            spec.config.mxnet.ps_resources[9]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4 + 2 * 9, 'limits': 2 + 3 * 4 + 4 * 9},
            'memory': {'requests': 300 + 256 * 4 + 512, 'limits': 300 + 256 * 4 + 1024},
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.SERVER: 10}, True)

    def test_distributed_mxnet_with_node_selectors_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/distributed_mxnet_with_node_selectors_file.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_experiment
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.environment.node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.master_node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.framework == ExperimentFramework.MXNET
        assert spec.config.mxnet.n_workers == 5
        assert spec.config.mxnet.n_ps == 10

        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert isinstance(spec.config.mxnet.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.config.mxnet.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.config.mxnet.default_worker_resources.cpu.requests == 3
        assert spec.config.mxnet.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.config.mxnet.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.config.mxnet.default_worker_resources.memory.requests == 256
        assert spec.config.mxnet.default_worker_resources.memory.limits == 256

        assert isinstance(spec.config.mxnet.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.config.mxnet.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.config.mxnet.worker_resources[3].memory.requests == 300
        assert spec.config.mxnet.worker_resources[3].memory.limits == 300

        assert isinstance(spec.config.mxnet.default_ps_resources,
                          PodResourcesConfig)
        assert isinstance(spec.config.mxnet.default_ps_resources.cpu,
                          K8SResourcesConfig)
        assert spec.config.mxnet.default_ps_resources.cpu.requests == 2
        assert spec.config.mxnet.default_ps_resources.cpu.limits == 4

        assert isinstance(spec.config.mxnet.ps_resources[9],
                          PodResourcesConfig)
        assert isinstance(spec.config.mxnet.ps_resources[9].memory,
                          K8SResourcesConfig)
        assert spec.config.mxnet.ps_resources[9].memory.requests == 512
        assert spec.config.mxnet.ps_resources[9].memory.limits == 1024

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = MXNetSpecification.get_worker_resources(
            environment=spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_resources) == spec.config.mxnet.n_workers
        assert set(worker_resources.values()) == {
            spec.config.mxnet.default_worker_resources,
            spec.config.mxnet.worker_resources[3]}

        ps_resources = MXNetSpecification.get_ps_resources(
            environment=spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_resources) == spec.config.mxnet.n_ps
        assert set(ps_resources.values()) == {
            spec.config.mxnet.default_ps_resources,
            spec.config.mxnet.ps_resources[9]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4 + 2 * 9, 'limits': 2 + 3 * 4 + 4 * 9},
            'memory': {'requests': 300 + 256 * 4 + 512, 'limits': 300 + 256 * 4 + 1024},
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.SERVER: 10}, True)

        assert (spec.config.mxnet.default_worker.node_selector ==
                {'polyaxon.com': 'node_for_worker_tasks'})
        assert (spec.config.mxnet.worker_node_selectors[2] ==
                {'polyaxon.com': 'node_for_worker_task_2'})

        assert (spec.config.mxnet.default_ps.node_selector ==
                {'polyaxon.com': 'node_for_ps_tasks'})
        assert (spec.config.mxnet.ps_node_selectors[2] ==
                {'polyaxon.com': 'node_for_ps_task_2'})

        worker_node_selectors = MXNetSpecification.get_worker_node_selectors(
            environment=spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_node_selectors) == spec.config.mxnet.n_workers
        assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
            tuple(spec.config.mxnet.default_worker.node_selector.items()),
            tuple(spec.config.mxnet.worker_node_selectors[2].items())}

        ps_node_selectors = MXNetSpecification.get_ps_node_selectors(
            environment=spec.config.mxnet,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_node_selectors) == spec.config.mxnet.n_ps
        assert set(tuple(i.items()) for i in ps_node_selectors.values()) == {
            tuple(spec.config.mxnet.default_ps.node_selector.items()),
            tuple(spec.config.mxnet.ps_node_selectors[2].items())}

    def test_notebook_job_with_node_selectors(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/notebook_with_custom_environment.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_notebook
        assert spec.is_notebook is True
        assert spec.backend is None
        assert spec.logging is None
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert isinstance(spec.build, BuildConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.artifact_refs == ['outputs1']
        assert spec.data_refs == ['data1', 'data2']
        assert spec.secret_refs == ['secret1', 'secret2']
        assert spec.config_map_refs == ['config_map1', 'config_map2']

        node_selector = {'polyaxon.com': 'node_for_notebook_jobs'}
        assert spec.environment.node_selector == node_selector
        assert spec.node_selector == node_selector

        resources = {
            'cpu': {'requests': 1, 'limits': 2},
            'memory': {'requests': 200, 'limits': 200},
        }
        assert spec.environment.resources.to_dict() == resources
        assert spec.resources.to_dict() == resources

        affinity = {
            'nodeAffinity': {'requiredDuringSchedulingIgnoredDuringExecution': {}}
        }
        assert spec.environment.affinity == affinity
        assert spec.affinity == affinity

        tolerations = [{'key': 'key', 'operator': 'Exists'}]

        assert spec.environment.tolerations == tolerations
        assert spec.tolerations == tolerations

    def test_jupyter_lab_job_with_node_selectors(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/jupyterlab_with_custom_environment.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_notebook
        assert spec.is_notebook is True
        assert spec.backend == 'lab'
        assert spec.logging is None
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert isinstance(spec.build, BuildConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.artifact_refs == ['outputs1']
        assert spec.data_refs == ['data1', 'data2']
        assert spec.secret_refs == ['secret1', 'secret2']
        assert spec.config_map_refs == ['config_map1', 'config_map2']

        node_selector = {'polyaxon.com': 'node_for_notebook_jobs'}
        assert spec.environment.node_selector == node_selector
        assert spec.node_selector == node_selector

        resources = {
            'cpu': {'requests': 1, 'limits': 2},
            'memory': {'requests': 200, 'limits': 200},
        }
        assert spec.environment.resources.to_dict() == resources
        assert spec.resources.to_dict() == resources

        affinity = {
            'nodeAffinity': {'requiredDuringSchedulingIgnoredDuringExecution': {}}
        }
        assert spec.environment.affinity == affinity
        assert spec.affinity == affinity

        tolerations = [{'key': 'key', 'operator': 'Exists'}]

        assert spec.environment.tolerations == tolerations
        assert spec.tolerations == tolerations

    def test_tensorboard_job_with_node_selectors(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/tensorboard_with_custom_environment.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_tensorboard
        assert spec.is_tensorboard is True
        assert spec.logging is None
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert isinstance(spec.build, BuildConfig)
        assert isinstance(spec.environment, EnvironmentConfig)

        node_selector = {'polyaxon.com': 'node_for_tensorboard_jobs'}
        assert spec.environment.node_selector == node_selector
        assert spec.node_selector == node_selector

        resources = {
            'cpu': {'requests': 1, 'limits': 2},
            'memory': {'requests': 200, 'limits': 200},
        }
        assert spec.environment.resources.to_dict() == resources
        assert spec.resources.to_dict() == resources

        affinity = {
            'nodeAffinity': {'requiredDuringSchedulingIgnoredDuringExecution': {}}
        }
        assert spec.environment.affinity == affinity
        assert spec.affinity == affinity

        tolerations = [{'key': 'key', 'operator': 'Exists'}]

        assert spec.environment.tolerations == tolerations
        assert spec.tolerations == tolerations

    def test_run_job_with_node_selectors(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/run_with_custom_environment.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_job
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert spec.logging is None
        assert isinstance(spec.build, BuildConfig)
        assert isinstance(spec.run, RunConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.artifact_refs == ['outputs1']
        assert spec.data_refs == ['data1', 'data2']
        assert spec.secret_refs == ['secret1', 'secret2']
        assert spec.config_map_refs == ['config_map1', 'config_map2']

        node_selector = {'polyaxon.com': 'node_for_jobs'}
        assert spec.environment.node_selector == node_selector
        assert spec.node_selector == node_selector

        resources = {
            'cpu': {'requests': 1, 'limits': 2},
            'memory': {'requests': 200, 'limits': 200},
        }
        assert spec.environment.resources.to_dict() == resources
        assert spec.resources.to_dict() == resources

        affinity = {
            'nodeAffinity': {'requiredDuringSchedulingIgnoredDuringExecution': {}}
        }
        assert spec.environment.affinity == affinity
        assert spec.affinity == affinity

        tolerations = [{'key': 'key', 'operator': 'Exists'}]

        assert spec.environment.tolerations == tolerations
        assert spec.tolerations == tolerations

    def test_build_job_with_custom_environment(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/build_with_custom_environment.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_build is True
        assert spec.logging is None
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert isinstance(spec.config, BuildConfig)
        assert isinstance(spec.environment, EnvironmentConfig)

        node_selector = {'polyaxon.com': 'node_for_build_jobs'}
        assert spec.environment.node_selector == node_selector
        assert spec.node_selector == node_selector

        resources = {
            'cpu': {'requests': 1, 'limits': 2},
            'memory': {'requests': 200, 'limits': 200},
        }
        assert spec.environment.resources.to_dict() == resources
        assert spec.resources.to_dict() == resources

        affinity = {
            'nodeAffinity': {'requiredDuringSchedulingIgnoredDuringExecution': {}}
        }
        assert spec.environment.affinity == affinity
        assert spec.affinity == affinity

        tolerations = [{'key': 'key', 'operator': 'Exists'}]

        assert spec.environment.tolerations == tolerations
        assert spec.tolerations == tolerations

    def test_build_job_with_context_and_dockerfile(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plain/build_with_context_and_dockerfile.yml'))
        spec = plxfile.specification
        spec.apply_context()
        assert spec.version == 1
        assert spec.is_build is True
        assert spec.logging is None
        assert spec.config.dockerfile == 'dockerfiles/Dockerfile'
        assert spec.config.context == 'module1'
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert isinstance(spec.environment, EnvironmentConfig)

        node_selector = {'polyaxon.com': 'node_for_build_jobs'}
        assert spec.environment.node_selector == node_selector
        assert spec.node_selector == node_selector

        resources = {
            'cpu': {'requests': 1, 'limits': 2},
            'memory': {'requests': 200, 'limits': 200},
        }
        assert spec.environment.resources.to_dict() == resources
        assert spec.resources.to_dict() == resources

        affinity = {
            'nodeAffinity': {'requiredDuringSchedulingIgnoredDuringExecution': {}}
        }
        assert spec.environment.affinity == affinity
        assert spec.affinity == affinity

        tolerations = [{'key': 'key', 'operator': 'Exists'}]

        assert spec.environment.tolerations == tolerations
        assert spec.tolerations == tolerations
