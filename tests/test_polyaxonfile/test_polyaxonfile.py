# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

from polyaxon_schemas.bridges import NoOpBridgeConfig
from polyaxon_schemas.build import BuildConfig
from polyaxon_schemas.environments import (
    EnvironmentConfig,
    K8SResourcesConfig,
    PodResourcesConfig,
    SessionConfig,
    TFRunConfig
)
from polyaxon_schemas.exceptions import PolyaxonfileError
from polyaxon_schemas.graph import GraphConfig
from polyaxon_schemas.hptuning import EarlyStoppingMetricConfig, HPTuningConfig
from polyaxon_schemas.logging import LoggingConfig
from polyaxon_schemas.losses import AbsoluteDifferenceConfig, MeanSquaredErrorConfig
from polyaxon_schemas.matrix import MatrixConfig
from polyaxon_schemas.models import ClassifierConfig, GeneratorConfig, RegressorConfig
from polyaxon_schemas.optimizers import AdamConfig
from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile
from polyaxon_schemas.polyaxonfile.specification.frameworks import (
    HorovodSpecification,
    MXNetSpecification,
    PytorchSpecification,
    TensorflowSpecification
)
from polyaxon_schemas.processing.pipelines import TFRecordImagePipelineConfig
from polyaxon_schemas.run_exec import RunConfig
from polyaxon_schemas.utils import Frameworks, SearchAlgorithms, TaskType


class TestPolyaxonfile(TestCase):
    def test_missing_version_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/missing_version.yml'))

    def test_missing_kind_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/missing_kind.yml'))

    def test_simple_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/simple_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.logging is None
        assert spec.tags is None
        assert spec.build is None
        assert spec.run is None
        assert spec.environment is None
        assert spec.framework is None
        assert spec.is_runnable
        assert spec.is_experiment
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert isinstance(spec.model, RegressorConfig)
        assert isinstance(spec.model.loss, MeanSquaredErrorConfig)
        assert isinstance(spec.model.optimizer, AdamConfig)
        assert isinstance(spec.model.graph, GraphConfig)
        assert len(spec.model.graph.layers) == 4
        assert spec.model.graph.input_layers == [['images', 0, 0]]
        last_layer = spec.model.graph.layers[-1].name
        assert spec.model.graph.output_layers == [[last_layer, 0, 0]]
        assert isinstance(spec.train.data_pipeline, TFRecordImagePipelineConfig)
        assert spec.eval is None

    def test_simple_generator_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/simple_generator_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.logging is None
        assert spec.build is None
        assert spec.run is None
        assert spec.environment is None
        assert spec.framework is None
        assert spec.is_runnable
        assert spec.is_experiment
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert isinstance(spec.model, GeneratorConfig)
        assert isinstance(spec.model.loss, MeanSquaredErrorConfig)
        assert isinstance(spec.model.optimizer, AdamConfig)
        assert isinstance(spec.model.encoder, GraphConfig)
        assert isinstance(spec.model.decoder, GraphConfig)
        assert isinstance(spec.model.bridge, NoOpBridgeConfig)
        assert isinstance(spec.train.data_pipeline, TFRecordImagePipelineConfig)
        assert spec.eval is None

    def test_advanced_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/advanced_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert isinstance(spec.logging, LoggingConfig)
        assert spec.is_runnable
        assert spec.is_experiment
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.framework == Frameworks.TENSORFLOW
        assert spec.environment.tensorflow.n_workers == 5
        assert spec.environment.tensorflow.n_ps == 10
        assert spec.environment.tensorflow.delay_workers_by_global_step is True
        assert isinstance(spec.environment.tensorflow.run_config, TFRunConfig)
        assert spec.environment.tensorflow.run_config.tf_random_seed == 100
        assert spec.environment.tensorflow.run_config.save_summary_steps == 100
        assert spec.environment.tensorflow.run_config.save_checkpoints_secs == 60
        assert isinstance(spec.environment.tensorflow.run_config.session, SessionConfig)
        assert spec.environment.tensorflow.run_config.session.allow_soft_placement is True
        assert spec.environment.tensorflow.run_config.session.intra_op_parallelism_threads == 2
        assert spec.environment.tensorflow.run_config.session.inter_op_parallelism_threads == 2

        # check properties for returning worker configs and resources
        assert spec.environment.tensorflow.worker_configs == {}
        assert spec.environment.tensorflow.ps_configs == {}
        assert spec.environment.tensorflow.worker_resources == {}
        assert spec.environment.tensorflow.ps_resources == {}

        cluster, is_distributed = spec.cluster_def

        assert TensorflowSpecification.get_worker_configs(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        ) == {}
        assert TensorflowSpecification.get_ps_configs(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        ) == {}
        assert TensorflowSpecification.get_worker_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        ) == {}
        assert TensorflowSpecification.get_ps_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        ) == {}

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.PS: 10}, True)

        assert isinstance(spec.model, ClassifierConfig)
        assert isinstance(spec.model.loss, MeanSquaredErrorConfig)
        assert isinstance(spec.model.optimizer, AdamConfig)
        assert spec.model.optimizer.learning_rate == 0.21
        assert isinstance(spec.model.graph, GraphConfig)
        assert len(spec.model.graph.layers) == 7
        assert spec.model.graph.input_layers == [['images', 0, 0]]
        assert len(spec.model.graph.output_layers) == 3
        assert ['super_dense', 0, 0] in spec.model.graph.output_layers
        assert isinstance(spec.train.data_pipeline, TFRecordImagePipelineConfig)
        assert len(spec.train.data_pipeline.feature_processors.feature_processors) == 1
        assert isinstance(spec.eval.data_pipeline, TFRecordImagePipelineConfig)
        assert spec.eval.data_pipeline.feature_processors is None

    def test_advanced_file_with_custom_configs_and_resources_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/advanced_file_with_custom_configs_and_resources.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert isinstance(spec.logging, LoggingConfig)
        assert spec.is_experiment
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
        assert spec.framework == Frameworks.TENSORFLOW
        assert spec.persistence.outputs == 'outputs1'
        assert spec.persistence.data == ['data1', 'data2']
        assert spec.environment.tensorflow.n_workers == 5
        assert spec.environment.tensorflow.n_ps == 10
        assert spec.environment.tensorflow.delay_workers_by_global_step is True
        assert isinstance(spec.environment.tensorflow.run_config, TFRunConfig)
        assert spec.environment.tensorflow.run_config.tf_random_seed == 100
        assert spec.environment.tensorflow.run_config.save_summary_steps == 100
        assert spec.environment.tensorflow.run_config.save_checkpoints_secs == 60

        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert isinstance(spec.environment.tensorflow.run_config.session, SessionConfig)
        assert spec.environment.tensorflow.run_config.session.allow_soft_placement is True
        assert spec.environment.tensorflow.run_config.session.intra_op_parallelism_threads == 2
        assert spec.environment.tensorflow.run_config.session.inter_op_parallelism_threads == 2

        assert isinstance(spec.environment.tensorflow.default_worker_config, SessionConfig)
        assert spec.environment.tensorflow.default_worker_config.allow_soft_placement is True
        assert spec.environment.tensorflow.default_worker_config.intra_op_parallelism_threads == 1
        assert spec.environment.tensorflow.default_worker_config.inter_op_parallelism_threads == 1

        assert spec.environment.tensorflow.worker_resources == {}
        assert spec.environment.tensorflow.worker_node_selectors == {}
        assert spec.environment.tensorflow.worker_affinities == {}
        assert isinstance(spec.environment.tensorflow.worker_tolerations[4], list)
        assert spec.environment.tensorflow.worker_tolerations[4] == [{
            'key': 'key',
            'operator': 'Exists',
            'effect': 'NoSchedule',
        }]
        assert isinstance(spec.environment.tensorflow.worker_configs[3], SessionConfig)
        assert spec.environment.tensorflow.worker_configs[3].allow_soft_placement is False
        assert spec.environment.tensorflow.worker_configs[3].intra_op_parallelism_threads == 5
        assert spec.environment.tensorflow.worker_configs[3].inter_op_parallelism_threads == 5

        assert isinstance(spec.environment.tensorflow.default_ps_resources, PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.default_ps_resources.cpu, K8SResourcesConfig)
        assert spec.environment.tensorflow.default_ps_resources.cpu.requests == 2
        assert spec.environment.tensorflow.default_ps_resources.cpu.limits == 4

        assert spec.environment.tensorflow.ps_configs == {}
        assert spec.environment.tensorflow.ps_node_selectors == {}
        assert isinstance(spec.environment.tensorflow.ps_tolerations[7], list)
        assert spec.environment.tensorflow.ps_tolerations[7] == [{
            'operator': 'Exists'
        }]
        assert isinstance(spec.environment.tensorflow.ps_affinities[7], dict)
        assert isinstance(spec.environment.tensorflow.ps_resources[9], PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.ps_resources[9].memory, K8SResourcesConfig)
        assert spec.environment.tensorflow.ps_resources[9].memory.requests == 512
        assert spec.environment.tensorflow.ps_resources[9].memory.limits == 1024

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_configs = TensorflowSpecification.get_worker_configs(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_configs) == spec.environment.tensorflow.n_workers
        assert set(worker_configs.values()) == {
            spec.environment.tensorflow.default_worker_config,
            spec.environment.tensorflow.worker_configs[3]}
        assert TensorflowSpecification.get_ps_configs(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        ) == {}

        assert TensorflowSpecification.get_worker_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        ) == {}
        ps_resources = TensorflowSpecification.get_ps_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_resources) == spec.environment.tensorflow.n_ps
        assert set(ps_resources.values()) == {
            spec.environment.tensorflow.default_ps_resources,
            spec.environment.tensorflow.ps_resources[9]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 2 * 9, 'limits': 2 + 4 * 9},
            'memory': {'requests': 512, 'limits': 1024},
            'gpu': None
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.PS: 10}, True)

        assert isinstance(spec.model, ClassifierConfig)
        assert isinstance(spec.model.loss, MeanSquaredErrorConfig)
        assert isinstance(spec.model.optimizer, AdamConfig)
        assert spec.model.optimizer.learning_rate == 0.21
        assert isinstance(spec.model.graph, GraphConfig)
        assert len(spec.model.graph.layers) == 7
        assert spec.model.graph.input_layers == [['images', 0, 0]]
        assert len(spec.model.graph.output_layers) == 3
        assert ['super_dense', 0, 0] in spec.model.graph.output_layers
        assert isinstance(spec.train.data_pipeline, TFRecordImagePipelineConfig)
        assert len(spec.train.data_pipeline.feature_processors.feature_processors) == 1
        assert isinstance(spec.eval.data_pipeline, TFRecordImagePipelineConfig)
        assert spec.eval.data_pipeline.feature_processors is None

    def test_matrix_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/matrix_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_group
        assert isinstance(spec.hptuning.matrix['lr'], MatrixConfig)
        assert isinstance(spec.hptuning.matrix['loss'], MatrixConfig)
        assert spec.hptuning.matrix['lr'].to_dict() == {
            'logspace': {'start': 0.01, 'stop': 0.1, 'num': 5}}
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

        spec = spec.get_experiment_spec(matrix_declaration=spec.matrix_declaration_test)
        assert spec.is_runnable
        assert spec.environment is not None
        assert spec.persistence.outputs == 'outputs1'
        assert spec.persistence.data == ['data1', 'data2']
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        model = spec.model
        assert isinstance(model, RegressorConfig)
        assert isinstance(model.loss, (MeanSquaredErrorConfig, AbsoluteDifferenceConfig))
        assert isinstance(model.optimizer, AdamConfig)
        assert isinstance(model.graph, GraphConfig)
        assert len(model.graph.layers) == 4
        assert model.graph.input_layers == [['images', 0, 0]]
        last_layer = model.graph.layers[-1].name
        assert model.graph.output_layers == [[last_layer, 0, 0]]
        assert isinstance(spec.train.data_pipeline, TFRecordImagePipelineConfig)

    def test_matrix_file_passes_int_float_types(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/matrix_file_with_int_float_types.yml'))
        spec = plxfile.specification
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

        spec = spec.get_experiment_spec(matrix_declaration=spec.matrix_declaration_test)
        assert spec.is_runnable
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        model = spec.model
        assert isinstance(model, RegressorConfig)
        assert model.optimizer.learning_rate in [3.3, 4.4]
        assert isinstance(model.graph, GraphConfig)
        assert len(model.graph.layers) == 4
        assert model.graph.input_layers == [['images', 0, 0]]
        assert model.graph.layers[1].pool_size in ([1, 1], [2, 2])

    def test_matrix_early_stopping_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/matrix_file_early_stopping.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_group
        assert isinstance(spec.hptuning.matrix['lr'], MatrixConfig)
        assert isinstance(spec.hptuning.matrix['loss'], MatrixConfig)
        assert spec.hptuning.matrix['lr'].to_dict() == {
            'logspace': {'start': 0.01, 'stop': 0.1, 'num': 5}}
        assert spec.hptuning.matrix['loss'].to_dict() == {'values': ['MeanSquaredError',
                                                                     'AbsoluteDifference']}
        assert spec.matrix_space == 10
        assert isinstance(spec.hptuning, HPTuningConfig)
        assert spec.hptuning.concurrency == 2
        assert spec.hptuning.random_search.n_experiments == 5
        assert spec.early_stopping == spec.hptuning.early_stopping
        assert len(spec.hptuning.early_stopping) == 1
        assert isinstance(spec.hptuning.early_stopping[0], EarlyStoppingMetricConfig)

        assert spec.experiments_def == {
            'search_algorithm': SearchAlgorithms.RANDOM,
            'early_stopping': True,
            'concurrency': 2,
            'n_experiments': 5
        }

        spec = spec.get_experiment_spec(matrix_declaration=spec.matrix_declaration_test)
        assert spec.is_runnable
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)

        model = spec.model
        assert isinstance(model, RegressorConfig)
        assert isinstance(model.loss, (MeanSquaredErrorConfig, AbsoluteDifferenceConfig))
        assert isinstance(model.optimizer, AdamConfig)
        assert isinstance(model.graph, GraphConfig)
        assert len(model.graph.layers) == 4
        assert model.graph.input_layers == [['images', 0, 0]]
        last_layer = model.graph.layers[-1].name
        assert model.graph.output_layers == [[last_layer, 0, 0]]
        assert isinstance(spec.train.data_pipeline, TFRecordImagePipelineConfig)

    def test_matrix_large_n_experiments_ignored_file_passes(self):
        plxfile = PolyaxonFile(
            os.path.abspath('tests/fixtures/matrix_file_ignored_n_experiments.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_group
        assert isinstance(spec.hptuning.matrix['lr'], MatrixConfig)
        assert isinstance(spec.hptuning.matrix['loss'], MatrixConfig)
        assert spec.hptuning.matrix['lr'].to_dict() == {
            'logspace': {'start': 0.01, 'stop': 0.1, 'num': 5}}
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

        spec = spec.get_experiment_spec(matrix_declaration=spec.matrix_declaration_test)
        assert spec.is_runnable
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)

        model = spec.model
        assert isinstance(model, RegressorConfig)
        assert isinstance(model.loss, (MeanSquaredErrorConfig, AbsoluteDifferenceConfig))
        assert isinstance(model.optimizer, AdamConfig)
        assert isinstance(model.graph, GraphConfig)
        assert len(model.graph.layers) == 4
        assert model.graph.input_layers == [['images', 0, 0]]
        last_layer = model.graph.layers[-1].name
        assert model.graph.output_layers == [[last_layer, 0, 0]]
        assert isinstance(spec.train.data_pipeline, TFRecordImagePipelineConfig)

    def test_one_matrix_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/one_matrix_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_group
        assert spec.hptuning is not None
        assert isinstance(spec.hptuning.matrix['loss'], MatrixConfig)
        assert spec.hptuning.matrix['loss'].to_dict() == {'values': ['MeanSquaredError',
                                                                     'AbsoluteDifference']}
        assert spec.matrix_space == 2

        spec = spec.get_experiment_spec(matrix_declaration=spec.matrix_declaration_test)
        assert spec.is_runnable
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        model = spec.model
        assert isinstance(model, RegressorConfig)
        assert isinstance(model.loss, (MeanSquaredErrorConfig, AbsoluteDifferenceConfig))
        assert isinstance(model.optimizer, AdamConfig)
        assert isinstance(model.graph, GraphConfig)
        assert len(model.graph.layers) == 4
        assert model.graph.input_layers == [['images', 0, 0]]
        last_layer = model.graph.layers[-1].name
        assert model.graph.output_layers == [[last_layer, 0, 0]]
        assert isinstance(spec.train.data_pipeline, TFRecordImagePipelineConfig)

    def test_run_simple_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/run_exec_simple_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.logging is None
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert spec.is_experiment
        assert isinstance(spec.build, BuildConfig)
        assert isinstance(spec.run, RunConfig)
        assert spec.is_runnable
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.model is None
        run = spec.run
        assert isinstance(run, RunConfig)
        assert run.cmd == "video_prediction_train --model=DNA --num_masks=1"

    def test_run_matrix_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/run_exec_matrix_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_group
        assert isinstance(spec.hptuning.matrix['model'], MatrixConfig)
        assert spec.hptuning.matrix['model'].to_dict() == {'values': ['CDNA', 'DNA', 'STP']}
        assert spec.matrix_space == 3
        assert isinstance(spec.hptuning, HPTuningConfig)
        declarations = spec.matrix_declaration_test
        spec = spec.get_experiment_spec(declarations)
        assert spec.is_runnable
        assert spec.environment is None
        assert spec.logging is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.model is None
        run = spec.run
        assert isinstance(run, RunConfig)
        declarations['num_masks'] = 1 if declarations['model'] == 'DNA' else 10
        assert run.cmd == ('video_prediction_train '
                           '--model="{model}" '
                           '--num_masks={num_masks}').format(
            **declarations
        )

    def test_run_matrix_sampling_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/run_exec_matrix_sampling_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_group
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
        declarations = spec.matrix_declaration_test
        spec = spec.get_experiment_spec(declarations)
        assert spec.is_runnable
        assert spec.environment is None
        assert spec.logging is not None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.model is None
        run = spec.run
        assert isinstance(run, RunConfig)
        declarations['num_masks'] = 1 if declarations['model'] == 'DNA' else 10
        assert run.cmd == ('video_prediction_train '
                           '--model="{model}" '
                           '--num_masks={num_masks}').format(
            **declarations
        )

    def test_distributed_tensorflow_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/distributed_tensorflow_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert isinstance(spec.logging, LoggingConfig)
        assert spec.is_experiment
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
        assert spec.environment.node_selector is None
        assert spec.master_node_selector is None
        assert spec.framework == Frameworks.TENSORFLOW
        assert spec.environment.tensorflow.n_workers == 5
        assert spec.environment.tensorflow.n_ps == 10

        assert spec.environment.tolerations is None
        assert spec.environment.node_selector is None
        assert isinstance(spec.environment.affinity, dict)
        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert spec.environment.tensorflow.default_worker_node_selector is None
        assert spec.environment.tensorflow.default_worker_affinity is None
        assert isinstance(spec.environment.tensorflow.default_worker_tolerations, list)
        assert isinstance(spec.environment.tensorflow.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.environment.tensorflow.default_worker_resources.cpu.requests == 3
        assert spec.environment.tensorflow.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.environment.tensorflow.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.environment.tensorflow.default_worker_resources.memory.requests == 256
        assert spec.environment.tensorflow.default_worker_resources.memory.limits == 256

        assert spec.environment.tensorflow.worker_tolerations[2] == [{'operator': 'Exists'}]
        assert isinstance(spec.environment.tensorflow.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.environment.tensorflow.worker_resources[3].memory.requests == 300
        assert spec.environment.tensorflow.worker_resources[3].memory.limits == 300

        assert spec.environment.tensorflow.default_ps_node_selector is None
        assert spec.environment.tensorflow.default_ps_affinity is None
        assert isinstance(spec.environment.tensorflow.default_ps_tolerations, list)
        assert isinstance(spec.environment.tensorflow.default_ps_resources, PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.default_ps_resources.cpu, K8SResourcesConfig)
        assert spec.environment.tensorflow.default_ps_resources.cpu.requests == 2
        assert spec.environment.tensorflow.default_ps_resources.cpu.limits == 4

        assert isinstance(spec.environment.tensorflow.ps_resources[9], PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.ps_resources[9].memory, K8SResourcesConfig)
        assert spec.environment.tensorflow.ps_resources[9].memory.requests == 512
        assert spec.environment.tensorflow.ps_resources[9].memory.limits == 1024

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_affinities = TensorflowSpecification.get_worker_affinities(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_tolerations = TensorflowSpecification.get_worker_tolerations(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_node_selectors = TensorflowSpecification.get_worker_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_resources = TensorflowSpecification.get_worker_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert worker_affinities == {}
        assert worker_node_selectors == {}
        assert len(worker_tolerations) == spec.environment.tensorflow.n_workers
        assert len(worker_resources) == spec.environment.tensorflow.n_workers
        assert set(worker_resources.values()) == {
            spec.environment.tensorflow.default_worker_resources,
            spec.environment.tensorflow.worker_resources[3]}

        ps_tolerations= TensorflowSpecification.get_ps_tolerations(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_affinities = TensorflowSpecification.get_ps_affinities(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_node_selectors = TensorflowSpecification.get_ps_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_resources = TensorflowSpecification.get_ps_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert ps_affinities == {}
        assert ps_node_selectors == {}
        assert len(ps_tolerations) == spec.environment.tensorflow.n_ps
        assert len(ps_resources) == spec.environment.tensorflow.n_ps
        assert set(ps_resources.values()) == {
            spec.environment.tensorflow.default_ps_resources,
            spec.environment.tensorflow.ps_resources[9]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4 + 2 * 9, 'limits': 2 + 3 * 4 + 4 * 9},
            'memory': {'requests': 300 + 256 * 4 + 512, 'limits': 300 + 256 * 4 + 1024},
            'gpu': None
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.PS: 10}, True)

    def test_distributed_tensorflow_passes_with_node_selectors(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/distributed_tensorflow_with_node_selectors_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_experiment
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
        assert spec.environment.node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.master_node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.framework == Frameworks.TENSORFLOW
        assert spec.environment.tensorflow.n_workers == 5
        assert spec.environment.tensorflow.n_ps == 10

        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert isinstance(spec.environment.tensorflow.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.environment.tensorflow.default_worker_resources.cpu.requests == 3
        assert spec.environment.tensorflow.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.environment.tensorflow.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.environment.tensorflow.default_worker_resources.memory.requests == 256
        assert spec.environment.tensorflow.default_worker_resources.memory.limits == 256

        assert isinstance(spec.environment.tensorflow.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.environment.tensorflow.worker_resources[3].memory.requests == 300
        assert spec.environment.tensorflow.worker_resources[3].memory.limits == 300

        assert isinstance(spec.environment.tensorflow.default_ps_resources, PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.default_ps_resources.cpu, K8SResourcesConfig)
        assert spec.environment.tensorflow.default_ps_resources.cpu.requests == 2
        assert spec.environment.tensorflow.default_ps_resources.cpu.limits == 4

        assert isinstance(spec.environment.tensorflow.ps_resources[9], PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.ps_resources[9].memory, K8SResourcesConfig)
        assert spec.environment.tensorflow.ps_resources[9].memory.requests == 512
        assert spec.environment.tensorflow.ps_resources[9].memory.limits == 1024

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = TensorflowSpecification.get_worker_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_resources) == spec.environment.tensorflow.n_workers
        assert set(worker_resources.values()) == {
            spec.environment.tensorflow.default_worker_resources,
            spec.environment.tensorflow.worker_resources[3]}

        ps_resources = TensorflowSpecification.get_ps_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_resources) == spec.environment.tensorflow.n_ps
        assert set(ps_resources.values()) == {
            spec.environment.tensorflow.default_ps_resources,
            spec.environment.tensorflow.ps_resources[9]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4 + 2 * 9, 'limits': 2 + 3 * 4 + 4 * 9},
            'memory': {'requests': 300 + 256 * 4 + 512, 'limits': 300 + 256 * 4 + 1024},
            'gpu': None
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.PS: 10}, True)

        assert (spec.environment.tensorflow.default_worker.node_selector ==
                {'polyaxon.com': 'node_for_worker_tasks'})
        assert (spec.environment.tensorflow.worker_node_selectors[2] ==
                {'polyaxon.com': 'node_for_worker_task_2'})

        assert (spec.environment.tensorflow.default_ps.node_selector ==
                {'polyaxon.com': 'node_for_ps_tasks'})
        assert (spec.environment.tensorflow.ps_node_selectors[2] ==
                {'polyaxon.com': 'node_for_ps_task_2'})

        worker_node_selectors = TensorflowSpecification.get_worker_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_node_selectors) == spec.environment.tensorflow.n_workers
        assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
            tuple(spec.environment.tensorflow.default_worker.node_selector.items()),
            tuple(spec.environment.tensorflow.worker_node_selectors[2].items())}

        ps_node_selectors = TensorflowSpecification.get_ps_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_node_selectors) == spec.environment.tensorflow.n_ps
        assert set(tuple(i.items()) for i in ps_node_selectors.values()) == {
            tuple(spec.environment.tensorflow.default_ps.node_selector.items()),
            tuple(spec.environment.tensorflow.ps_node_selectors[2].items())}

    def test_distributed_horovod_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/distributed_horovod_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_experiment
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
        assert spec.framework == Frameworks.HOROVOD
        assert spec.environment.horovod.n_workers == 5

        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert isinstance(spec.environment.horovod.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.environment.horovod.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.environment.horovod.default_worker_resources.cpu.requests == 3
        assert spec.environment.horovod.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.environment.horovod.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.environment.horovod.default_worker_resources.memory.requests == 256
        assert spec.environment.horovod.default_worker_resources.memory.limits == 256

        assert isinstance(spec.environment.horovod.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.environment.horovod.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.environment.horovod.worker_resources[3].memory.requests == 300
        assert spec.environment.horovod.worker_resources[3].memory.limits == 300

        assert isinstance(spec.environment.affinity, dict)
        assert spec.environment.horovod.worker_affinities == {}

        assert spec.environment.tolerations is None
        assert isinstance(spec.environment.horovod.default_worker_tolerations, list)
        assert isinstance(spec.environment.horovod.worker_tolerations[2], list)
        assert spec.environment.horovod.worker_tolerations[2] == [{'operator': 'Exists'}]

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = HorovodSpecification.get_worker_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_node_selectors = HorovodSpecification.get_worker_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_affinities = HorovodSpecification.get_worker_affinities(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_tolerations = HorovodSpecification.get_worker_tolerations(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )

        assert worker_node_selectors == {}
        assert worker_affinities == {}
        assert len(worker_tolerations) == spec.environment.horovod.n_workers
        assert len(worker_resources) == spec.environment.horovod.n_workers
        assert set(worker_resources.values()) == {
            spec.environment.horovod.default_worker_resources,
            spec.environment.horovod.worker_resources[3]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4, 'limits': 2 + 3 * 4},
            'memory': {'requests': 300 + 256 * 4, 'limits': 300 + 256 * 4},
            'gpu': None
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5}, True)

    def test_distributed_horovod_with_node_selectors_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/distributed_horovod_with_node_selectors_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_experiment
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
        assert spec.environment.node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.master_node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.framework == Frameworks.HOROVOD
        assert spec.environment.horovod.n_workers == 5

        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert isinstance(spec.environment.horovod.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.environment.horovod.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.environment.horovod.default_worker_resources.cpu.requests == 3
        assert spec.environment.horovod.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.environment.horovod.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.environment.horovod.default_worker_resources.memory.requests == 256
        assert spec.environment.horovod.default_worker_resources.memory.limits == 256

        assert isinstance(spec.environment.horovod.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.environment.horovod.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.environment.horovod.worker_resources[3].memory.requests == 300
        assert spec.environment.horovod.worker_resources[3].memory.limits == 300

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = HorovodSpecification.get_worker_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_resources) == spec.environment.horovod.n_workers
        assert set(worker_resources.values()) == {
            spec.environment.horovod.default_worker_resources,
            spec.environment.horovod.worker_resources[3]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4, 'limits': 2 + 3 * 4},
            'memory': {'requests': 300 + 256 * 4, 'limits': 300 + 256 * 4},
            'gpu': None
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5}, True)

        assert (spec.environment.horovod.default_worker.node_selector ==
                {'polyaxon.com': 'node_for_worker_tasks'})
        assert (spec.environment.horovod.worker_node_selectors[2] ==
                {'polyaxon.com': 'node_for_worker_task_2'})

        worker_node_selectors = HorovodSpecification.get_worker_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_node_selectors) == spec.environment.horovod.n_workers
        assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
            tuple(spec.environment.horovod.default_worker.node_selector.items()),
            tuple(spec.environment.horovod.worker_node_selectors[2].items())}

    def test_distributed_pytorch_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/distributed_pytorch_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_experiment
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
        assert spec.framework == Frameworks.PYTORCH
        assert spec.environment.pytorch.n_workers == 5

        assert spec.environment.node_selector is None
        assert spec.environment.tolerations is None
        assert isinstance(spec.environment.affinity, dict)
        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert spec.environment.pytorch.default_worker_node_selector is None
        assert spec.environment.pytorch.default_worker_affinity is None
        assert isinstance(spec.environment.pytorch.default_worker_tolerations, list)
        assert isinstance(spec.environment.pytorch.default_worker_tolerations[0], dict)
        assert isinstance(spec.environment.pytorch.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.environment.pytorch.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.environment.pytorch.default_worker_resources.cpu.requests == 3
        assert spec.environment.pytorch.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.environment.pytorch.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.environment.pytorch.default_worker_resources.memory.requests == 256
        assert spec.environment.pytorch.default_worker_resources.memory.limits == 256

        assert spec.environment.pytorch.worker_tolerations[2] == [{'operator': 'Exists'}]
        assert isinstance(spec.environment.pytorch.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.environment.pytorch.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.environment.pytorch.worker_resources[3].memory.requests == 300
        assert spec.environment.pytorch.worker_resources[3].memory.limits == 300

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = PytorchSpecification.get_worker_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_tolerations = PytorchSpecification.get_worker_tolerations(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_node_selectors = PytorchSpecification.get_worker_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_affinities = PytorchSpecification.get_worker_affinities(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert worker_node_selectors == {}
        assert worker_affinities == {}
        assert len(worker_tolerations) == spec.environment.pytorch.n_workers
        assert len(worker_resources) == spec.environment.pytorch.n_workers
        assert set(worker_resources.values()) == {
            spec.environment.pytorch.default_worker_resources,
            spec.environment.pytorch.worker_resources[3]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4, 'limits': 2 + 3 * 4},
            'memory': {'requests': 300 + 256 * 4, 'limits': 300 + 256 * 4},
            'gpu': None
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5}, True)

    def test_distributed_pytorch_with_node_selectors_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/distributed_pytorch_with_node_selectors_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_experiment
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
        assert spec.environment.node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.master_node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.framework == Frameworks.PYTORCH
        assert spec.environment.pytorch.n_workers == 5

        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert isinstance(spec.environment.pytorch.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.environment.pytorch.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.environment.pytorch.default_worker_resources.cpu.requests == 3
        assert spec.environment.pytorch.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.environment.pytorch.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.environment.pytorch.default_worker_resources.memory.requests == 256
        assert spec.environment.pytorch.default_worker_resources.memory.limits == 256

        assert isinstance(spec.environment.pytorch.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.environment.pytorch.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.environment.pytorch.worker_resources[3].memory.requests == 300
        assert spec.environment.pytorch.worker_resources[3].memory.limits == 300

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = PytorchSpecification.get_worker_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_resources) == spec.environment.pytorch.n_workers
        assert set(worker_resources.values()) == {
            spec.environment.pytorch.default_worker_resources,
            spec.environment.pytorch.worker_resources[3]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4, 'limits': 2 + 3 * 4},
            'memory': {'requests': 300 + 256 * 4, 'limits': 300 + 256 * 4},
            'gpu': None
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5}, True)

        assert (spec.environment.pytorch.default_worker.node_selector ==
                {'polyaxon.com': 'node_for_worker_tasks'})
        assert (spec.environment.pytorch.worker_node_selectors[2] ==
                {'polyaxon.com': 'node_for_worker_task_2'})

        worker_node_selectors = PytorchSpecification.get_worker_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_node_selectors) == spec.environment.pytorch.n_workers
        assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
            tuple(spec.environment.pytorch.default_worker.node_selector.items()),
            tuple(spec.environment.pytorch.worker_node_selectors[2].items())}

    def test_distributed_mxnet_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/distributed_mxnet_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_experiment
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
        assert spec.framework == Frameworks.MXNET
        assert spec.environment.mxnet.n_workers == 5
        assert spec.environment.mxnet.n_ps == 10

        assert spec.environment.node_selector is None
        assert spec.environment.tolerations is None
        assert isinstance(spec.environment.affinity, dict)
        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert spec.environment.mxnet.default_worker_node_selector is None
        assert spec.environment.mxnet.default_worker_affinity is None
        assert isinstance(spec.environment.mxnet.default_worker_tolerations, list)
        assert isinstance(spec.environment.mxnet.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.environment.mxnet.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.default_worker_resources.cpu.requests == 3
        assert spec.environment.mxnet.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.environment.mxnet.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.default_worker_resources.memory.requests == 256
        assert spec.environment.mxnet.default_worker_resources.memory.limits == 256

        assert isinstance(spec.environment.mxnet.worker_tolerations[2], list)
        assert spec.environment.mxnet.worker_tolerations[2] == [{'operator': 'Exists'}]
        assert isinstance(spec.environment.mxnet.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.environment.mxnet.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.worker_resources[3].memory.requests == 300
        assert spec.environment.mxnet.worker_resources[3].memory.limits == 300

        assert spec.environment.mxnet.default_ps_node_selector is None
        assert spec.environment.mxnet.default_ps_affinity is None
        assert isinstance(spec.environment.mxnet.default_ps_tolerations, list)
        assert isinstance(spec.environment.mxnet.default_ps_resources,
                          PodResourcesConfig)
        assert isinstance(spec.environment.mxnet.default_ps_resources.cpu,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.default_ps_resources.cpu.requests == 2
        assert spec.environment.mxnet.default_ps_resources.cpu.limits == 4

        assert isinstance(spec.environment.mxnet.ps_resources[9],
                          PodResourcesConfig)
        assert isinstance(spec.environment.mxnet.ps_resources[9].memory,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.ps_resources[9].memory.requests == 512
        assert spec.environment.mxnet.ps_resources[9].memory.limits == 1024

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = MXNetSpecification.get_worker_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_node_selectors = MXNetSpecification.get_worker_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_affinities = MXNetSpecification.get_worker_affinities(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        worker_tolerations = MXNetSpecification.get_worker_tolerations(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert worker_node_selectors == {}
        assert worker_affinities == {}
        assert len(worker_tolerations) == spec.environment.mxnet.n_workers
        assert len(worker_resources) == spec.environment.mxnet.n_workers
        assert set(worker_resources.values()) == {
            spec.environment.mxnet.default_worker_resources,
            spec.environment.mxnet.worker_resources[3]}

        ps_resources = MXNetSpecification.get_ps_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_node_selectors = MXNetSpecification.get_ps_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_affinities = MXNetSpecification.get_ps_affinities(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        ps_tolerations = MXNetSpecification.get_ps_tolerations(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert ps_node_selectors == {}
        assert ps_affinities == {}
        assert len(ps_tolerations) == spec.environment.mxnet.n_ps
        assert len(ps_resources) == spec.environment.mxnet.n_ps
        assert set(ps_resources.values()) == {
            spec.environment.mxnet.default_ps_resources,
            spec.environment.mxnet.ps_resources[9]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4 + 2 * 9, 'limits': 2 + 3 * 4 + 4 * 9},
            'memory': {'requests': 300 + 256 * 4 + 512, 'limits': 300 + 256 * 4 + 1024},
            'gpu': None
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.SERVER: 10}, True)

    def test_distributed_mxnet_with_node_selectors_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/distributed_mxnet_with_node_selectors_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_experiment
        assert isinstance(spec.logging, LoggingConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
        assert spec.environment.node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.master_node_selector == {'polyaxon.com': 'node_for_master_task'}
        assert spec.framework == Frameworks.MXNET
        assert spec.environment.mxnet.n_workers == 5
        assert spec.environment.mxnet.n_ps == 10

        assert isinstance(spec.environment.resources, PodResourcesConfig)
        assert isinstance(spec.environment.resources.cpu, K8SResourcesConfig)
        assert spec.environment.resources.cpu.requests == 1
        assert spec.environment.resources.cpu.limits == 2

        assert isinstance(spec.environment.mxnet.default_worker_resources,
                          PodResourcesConfig)
        assert isinstance(spec.environment.mxnet.default_worker_resources.cpu,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.default_worker_resources.cpu.requests == 3
        assert spec.environment.mxnet.default_worker_resources.cpu.limits == 3
        assert isinstance(spec.environment.mxnet.default_worker_resources.memory,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.default_worker_resources.memory.requests == 256
        assert spec.environment.mxnet.default_worker_resources.memory.limits == 256

        assert isinstance(spec.environment.mxnet.worker_resources[3], PodResourcesConfig)
        assert isinstance(spec.environment.mxnet.worker_resources[3].memory,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.worker_resources[3].memory.requests == 300
        assert spec.environment.mxnet.worker_resources[3].memory.limits == 300

        assert isinstance(spec.environment.mxnet.default_ps_resources,
                          PodResourcesConfig)
        assert isinstance(spec.environment.mxnet.default_ps_resources.cpu,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.default_ps_resources.cpu.requests == 2
        assert spec.environment.mxnet.default_ps_resources.cpu.limits == 4

        assert isinstance(spec.environment.mxnet.ps_resources[9],
                          PodResourcesConfig)
        assert isinstance(spec.environment.mxnet.ps_resources[9].memory,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.ps_resources[9].memory.requests == 512
        assert spec.environment.mxnet.ps_resources[9].memory.limits == 1024

        # check that properties for return list of configs and resources is working
        cluster, is_distributed = spec.cluster_def
        worker_resources = MXNetSpecification.get_worker_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_resources) == spec.environment.mxnet.n_workers
        assert set(worker_resources.values()) == {
            spec.environment.mxnet.default_worker_resources,
            spec.environment.mxnet.worker_resources[3]}

        ps_resources = MXNetSpecification.get_ps_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_resources) == spec.environment.mxnet.n_ps
        assert set(ps_resources.values()) == {
            spec.environment.mxnet.default_ps_resources,
            spec.environment.mxnet.ps_resources[9]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4 + 2 * 9, 'limits': 2 + 3 * 4 + 4 * 9},
            'memory': {'requests': 300 + 256 * 4 + 512, 'limits': 300 + 256 * 4 + 1024},
            'gpu': None
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.SERVER: 10}, True)

        assert (spec.environment.mxnet.default_worker.node_selector ==
                {'polyaxon.com': 'node_for_worker_tasks'})
        assert (spec.environment.mxnet.worker_node_selectors[2] ==
                {'polyaxon.com': 'node_for_worker_task_2'})

        assert (spec.environment.mxnet.default_ps.node_selector ==
                {'polyaxon.com': 'node_for_ps_tasks'})
        assert (spec.environment.mxnet.ps_node_selectors[2] ==
                {'polyaxon.com': 'node_for_ps_task_2'})

        worker_node_selectors = MXNetSpecification.get_worker_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_node_selectors) == spec.environment.mxnet.n_workers
        assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
            tuple(spec.environment.mxnet.default_worker.node_selector.items()),
            tuple(spec.environment.mxnet.worker_node_selectors[2].items())}

        ps_node_selectors = MXNetSpecification.get_ps_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_node_selectors) == spec.environment.mxnet.n_ps
        assert set(tuple(i.items()) for i in ps_node_selectors.values()) == {
            tuple(spec.environment.mxnet.default_ps.node_selector.items()),
            tuple(spec.environment.mxnet.ps_node_selectors[2].items())}

    def test_notebook_job_with_node_selectors(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/notebook_with_custom_environment.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_notebook
        assert spec.is_notebook is True
        assert spec.logging is None
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert isinstance(spec.build, BuildConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.persistence.outputs == 'outputs1'
        assert spec.persistence.data == ['data1', 'data2']

        node_selector = {'polyaxon.com': 'node_for_notebook_jobs'}
        assert spec.environment.node_selector == node_selector
        assert spec.node_selector == node_selector

        resources = {
            'cpu': {'requests': 1, 'limits': 2},
            'memory': {'requests': 200, 'limits': 200},
            'gpu': None
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
            'tests/fixtures/tensorboard_with_custom_environment.yml'))
        spec = plxfile.specification
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
            'gpu': None
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
            'tests/fixtures/run_with_custom_environment.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_job
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert spec.logging is None
        assert isinstance(spec.build, BuildConfig)
        assert isinstance(spec.run, RunConfig)
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.persistence.outputs == 'outputs1'
        assert spec.persistence.data == ['data1', 'data2']

        node_selector = {'polyaxon.com': 'node_for_jobs'}
        assert spec.environment.node_selector == node_selector
        assert spec.node_selector == node_selector

        resources = {
            'cpu': {'requests': 1, 'limits': 2},
            'memory': {'requests': 200, 'limits': 200},
            'gpu': None
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
            'tests/fixtures/build_with_custom_environment.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.is_build is True
        assert spec.logging is None
        assert sorted(spec.tags) == sorted(['foo', 'bar'])
        assert isinstance(spec.build, BuildConfig)
        assert isinstance(spec.environment, EnvironmentConfig)

        node_selector = {'polyaxon.com': 'node_for_build_jobs'}
        assert spec.environment.node_selector == node_selector
        assert spec.node_selector == node_selector

        resources = {
            'cpu': {'requests': 1, 'limits': 2},
            'memory': {'requests': 200, 'limits': 200},
            'gpu': None
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
