# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

from polyaxon_schemas.bridges import NoOpBridgeConfig
from polyaxon_schemas.environments import (
    EnvironmentConfig,
    K8SResourcesConfig,
    PodResourcesConfig,
    RunConfig,
    SessionConfig
)
from polyaxon_schemas.exceptions import PolyaxonfileError
from polyaxon_schemas.graph import GraphConfig
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
from polyaxon_schemas.run_exec import RunExecConfig
from polyaxon_schemas.settings import EarlyStoppingMetricConfig, SettingsConfig
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
        assert spec.settings is None
        assert spec.environment is None
        assert spec.framework is None
        assert spec.is_runnable
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
        assert spec.settings is None
        assert spec.environment is None
        assert spec.framework is None
        assert spec.is_runnable
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
        assert isinstance(spec.settings, SettingsConfig)
        assert isinstance(spec.settings.logging, LoggingConfig)
        assert spec.settings.matrix is None
        assert spec.is_runnable
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.framework == Frameworks.TENSORFLOW
        assert spec.environment.tensorflow.n_workers == 5
        assert spec.environment.tensorflow.n_ps == 10
        assert spec.environment.tensorflow.delay_workers_by_global_step is True
        assert isinstance(spec.environment.tensorflow.run_config, RunConfig)
        assert spec.environment.tensorflow.run_config.tf_random_seed == 100
        assert spec.environment.tensorflow.run_config.save_summary_steps == 100
        assert spec.environment.tensorflow.run_config.save_checkpoints_secs == 60
        assert isinstance(spec.environment.tensorflow.run_config.session, SessionConfig)
        assert spec.environment.tensorflow.run_config.session.allow_soft_placement is True
        assert spec.environment.tensorflow.run_config.session.intra_op_parallelism_threads == 2
        assert spec.environment.tensorflow.run_config.session.inter_op_parallelism_threads == 2

        # check properties for returning worker configs and resources
        assert spec.environment.tensorflow.worker_configs is None
        assert spec.environment.tensorflow.ps_configs is None
        assert spec.environment.tensorflow.worker_resources is None
        assert spec.environment.tensorflow.ps_resources is None

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
        assert isinstance(spec.settings, SettingsConfig)
        assert isinstance(spec.settings.logging, LoggingConfig)
        assert spec.settings.matrix is None
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
        assert spec.framework == Frameworks.TENSORFLOW
        assert spec.environment.tensorflow.n_workers == 5
        assert spec.environment.tensorflow.n_ps == 10
        assert spec.environment.tensorflow.delay_workers_by_global_step is True
        assert isinstance(spec.environment.tensorflow.run_config, RunConfig)
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

        assert isinstance(spec.environment.tensorflow.worker_configs[0], SessionConfig)
        assert spec.environment.tensorflow.worker_configs[0].index == 3
        assert spec.environment.tensorflow.worker_configs[0].allow_soft_placement is False
        assert spec.environment.tensorflow.worker_configs[0].intra_op_parallelism_threads == 5
        assert spec.environment.tensorflow.worker_configs[0].inter_op_parallelism_threads == 5

        assert spec.environment.tensorflow.ps_configs is None

        assert spec.environment.tensorflow.worker_resources is None

        assert isinstance(spec.environment.tensorflow.default_ps_resources, PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.default_ps_resources.cpu, K8SResourcesConfig)
        assert spec.environment.tensorflow.default_ps_resources.cpu.requests == 2
        assert spec.environment.tensorflow.default_ps_resources.cpu.limits == 4

        assert isinstance(spec.environment.tensorflow.ps_resources[0], PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.ps_resources[0].memory, K8SResourcesConfig)
        assert spec.environment.tensorflow.ps_resources[0].index == 9
        assert spec.environment.tensorflow.ps_resources[0].memory.requests == 512
        assert spec.environment.tensorflow.ps_resources[0].memory.limits == 1024

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
            spec.environment.tensorflow.worker_configs[0]}
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
            spec.environment.tensorflow.ps_resources[0]}

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
        assert isinstance(spec.settings.matrix['lr'], MatrixConfig)
        assert isinstance(spec.settings.matrix['loss'], MatrixConfig)
        assert spec.settings.matrix['lr'].to_dict() == {
            'logspace': {'start': 0.01, 'stop': 0.1, 'num': 5}}
        assert spec.settings.matrix['loss'].to_dict() == {'values': ['MeanSquaredError',
                                                                     'AbsoluteDifference']}
        assert spec.matrix_space == 10
        assert isinstance(spec.settings, SettingsConfig)
        assert spec.settings.concurrency == 2
        assert spec.search_algorithm == SearchAlgorithms.GRID
        assert spec.settings.early_stopping is None
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
        assert isinstance(spec.settings.matrix['param1'], MatrixConfig)
        assert isinstance(spec.settings.matrix['param2'], MatrixConfig)
        assert spec.settings.matrix['param1'].to_dict() == {'values': [1, 2]}
        assert spec.settings.matrix['param2'].to_dict() == {'values': [3.3, 4.4]}
        assert spec.matrix_space == 4
        assert isinstance(spec.settings, SettingsConfig)
        assert spec.settings.concurrency == 2
        assert spec.search_algorithm == SearchAlgorithms.GRID
        assert spec.settings.early_stopping is None
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
        assert isinstance(spec.settings.matrix['lr'], MatrixConfig)
        assert isinstance(spec.settings.matrix['loss'], MatrixConfig)
        assert spec.settings.matrix['lr'].to_dict() == {
            'logspace': {'start': 0.01, 'stop': 0.1, 'num': 5}}
        assert spec.settings.matrix['loss'].to_dict() == {'values': ['MeanSquaredError',
                                                                     'AbsoluteDifference']}
        assert spec.matrix_space == 10
        assert isinstance(spec.settings, SettingsConfig)
        assert spec.settings.concurrency == 2
        assert spec.settings.random_search.n_experiments == 5
        assert spec.early_stopping == spec.settings.early_stopping
        assert len(spec.settings.early_stopping) == 1
        assert isinstance(spec.settings.early_stopping[0], EarlyStoppingMetricConfig)

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
        assert isinstance(spec.settings.matrix['lr'], MatrixConfig)
        assert isinstance(spec.settings.matrix['loss'], MatrixConfig)
        assert spec.settings.matrix['lr'].to_dict() == {
            'logspace': {'start': 0.01, 'stop': 0.1, 'num': 5}}
        assert spec.settings.matrix['loss'].to_dict() == {'values': ['MeanSquaredError',
                                                                     'AbsoluteDifference']}
        assert spec.matrix_space == 10
        assert isinstance(spec.settings, SettingsConfig)
        assert spec.settings.concurrency == 2
        assert spec.search_algorithm == SearchAlgorithms.RANDOM
        assert spec.settings.random_search.n_experiments == 300
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
        assert spec.settings is not None
        assert isinstance(spec.settings.matrix['loss'], MatrixConfig)
        assert spec.settings.matrix['loss'].to_dict() == {'values': ['MeanSquaredError',
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
        assert spec.settings is None
        assert spec.is_runnable
        assert spec.environment is None
        assert spec.framework is None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.model is None
        run_exec = spec.run_exec
        assert isinstance(run_exec, RunExecConfig)
        assert run_exec.cmd == "video_prediction_train --model=DNA --num_masks=1"

    def test_run_matrix_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/run_exec_matrix_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert isinstance(spec.settings.matrix['model'], MatrixConfig)
        assert spec.settings.matrix['model'].to_dict() == {'values': ['CDNA', 'DNA', 'STP']}
        assert spec.matrix_space == 3
        assert isinstance(spec.settings, SettingsConfig)
        declarations = spec.matrix_declaration_test
        spec = spec.get_experiment_spec(declarations)
        assert spec.is_runnable
        assert spec.environment is None
        assert spec.settings is not None
        assert spec.settings.logging is not None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.model is None
        run_exec = spec.run_exec
        assert isinstance(run_exec, RunExecConfig)
        declarations['num_masks'] = 1 if declarations['model'] == 'DNA' else 10
        assert run_exec.cmd == ('video_prediction_train '
                                '--model="{model}" '
                                '--num_masks={num_masks}').format(
            **declarations
        )

    def test_run_matrix_sampling_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/run_exec_matrix_sampling_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert isinstance(spec.settings.matrix['model'], MatrixConfig)
        assert spec.settings.matrix['learning_rate'].to_dict() == {
            'normal': {'loc': 0, 'scale': 0.9}}
        assert spec.settings.matrix['dropout'].to_dict() == {
            'qloguniform': {'high': 0.8, 'low': 0, 'q': 0.1}}
        assert spec.settings.matrix['activation'].to_dict() == {
            'pvalues': [['relu', 0.1], ['sigmoid', 0.8]]}
        assert spec.settings.matrix['model'].to_dict() == {'values': ['CDNA', 'DNA', 'STP']}
        assert isinstance(spec.settings, SettingsConfig)
        declarations = spec.matrix_declaration_test
        spec = spec.get_experiment_spec(declarations)
        assert spec.is_runnable
        assert spec.environment is None
        assert spec.settings is not None
        assert spec.settings.logging is not None
        assert spec.cluster_def == ({TaskType.MASTER: 1}, False)
        assert spec.model is None
        run_exec = spec.run_exec
        assert isinstance(run_exec, RunExecConfig)
        declarations['num_masks'] = 1 if declarations['model'] == 'DNA' else 10
        assert run_exec.cmd == ('video_prediction_train '
                                '--model="{model}" '
                                '--num_masks={num_masks}').format(
            **declarations
        )

    def test_distributed_tensorflow_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/distributed_tensorflow_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert isinstance(spec.settings, SettingsConfig)
        assert isinstance(spec.settings.logging, LoggingConfig)
        assert spec.settings.matrix is None
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
        assert spec.environment.node_selectors is None
        assert spec.master_node_selectors is None
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

        assert isinstance(spec.environment.tensorflow.worker_resources[0], PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.worker_resources[0].memory,
                          K8SResourcesConfig)
        assert spec.environment.tensorflow.worker_resources[0].index == 3
        assert spec.environment.tensorflow.worker_resources[0].memory.requests == 300
        assert spec.environment.tensorflow.worker_resources[0].memory.limits == 300

        assert isinstance(spec.environment.tensorflow.default_ps_resources, PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.default_ps_resources.cpu, K8SResourcesConfig)
        assert spec.environment.tensorflow.default_ps_resources.cpu.requests == 2
        assert spec.environment.tensorflow.default_ps_resources.cpu.limits == 4

        assert isinstance(spec.environment.tensorflow.ps_resources[0], PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.ps_resources[0].memory, K8SResourcesConfig)
        assert spec.environment.tensorflow.ps_resources[0].index == 9
        assert spec.environment.tensorflow.ps_resources[0].memory.requests == 512
        assert spec.environment.tensorflow.ps_resources[0].memory.limits == 1024

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
            spec.environment.tensorflow.worker_resources[0]}

        ps_resources = TensorflowSpecification.get_ps_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_resources) == spec.environment.tensorflow.n_ps
        assert set(ps_resources.values()) == {
            spec.environment.tensorflow.default_ps_resources,
            spec.environment.tensorflow.ps_resources[0]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4 + 2 * 9, 'limits': 2 + 3 * 4 + 4 * 9},
            'memory': {'requests': 300 + 256 * 4 + 512, 'limits': 300 + 256 * 4 + 1024},
            'gpu': None
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.PS: 10}, True)

    def test_distributed_tensorflow_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/distributed_tensorflow_with_node_selectors_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert isinstance(spec.settings, SettingsConfig)
        assert isinstance(spec.settings.logging, LoggingConfig)
        assert spec.settings.matrix is None
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
        assert spec.environment.node_selectors == {'polyaxon.com': 'node_for_master_task'}
        assert spec.master_node_selectors == {'polyaxon.com': 'node_for_master_task'}
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

        assert isinstance(spec.environment.tensorflow.worker_resources[0], PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.worker_resources[0].memory,
                          K8SResourcesConfig)
        assert spec.environment.tensorflow.worker_resources[0].index == 3
        assert spec.environment.tensorflow.worker_resources[0].memory.requests == 300
        assert spec.environment.tensorflow.worker_resources[0].memory.limits == 300

        assert isinstance(spec.environment.tensorflow.default_ps_resources, PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.default_ps_resources.cpu, K8SResourcesConfig)
        assert spec.environment.tensorflow.default_ps_resources.cpu.requests == 2
        assert spec.environment.tensorflow.default_ps_resources.cpu.limits == 4

        assert isinstance(spec.environment.tensorflow.ps_resources[0], PodResourcesConfig)
        assert isinstance(spec.environment.tensorflow.ps_resources[0].memory, K8SResourcesConfig)
        assert spec.environment.tensorflow.ps_resources[0].index == 9
        assert spec.environment.tensorflow.ps_resources[0].memory.requests == 512
        assert spec.environment.tensorflow.ps_resources[0].memory.limits == 1024

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
            spec.environment.tensorflow.worker_resources[0]}

        ps_resources = TensorflowSpecification.get_ps_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_resources) == spec.environment.tensorflow.n_ps
        assert set(ps_resources.values()) == {
            spec.environment.tensorflow.default_ps_resources,
            spec.environment.tensorflow.ps_resources[0]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4 + 2 * 9, 'limits': 2 + 3 * 4 + 4 * 9},
            'memory': {'requests': 300 + 256 * 4 + 512, 'limits': 300 + 256 * 4 + 1024},
            'gpu': None
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.PS: 10}, True)

        assert (spec.environment.tensorflow.default_worker_node_selectors ==
                {'polyaxon.com': 'node_for_worker_tasks'})
        assert (spec.environment.tensorflow.worker_node_selectors[0] ==
                {'index': 2, 'polyaxon.com': 'node_for_worker_task_2'})

        assert (spec.environment.tensorflow.default_ps_node_selectors ==
                {'polyaxon.com': 'node_for_ps_tasks'})
        assert (spec.environment.tensorflow.ps_node_selectors[0] ==
                {'index': 2, 'polyaxon.com': 'node_for_ps_task_2'})

        worker_node_selectors = TensorflowSpecification.get_worker_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_node_selectors) == spec.environment.tensorflow.n_workers
        assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
            tuple(spec.environment.tensorflow.default_worker_node_selectors.items()),
            tuple(spec.environment.tensorflow.worker_node_selectors[0].items())}

        ps_node_selectors = TensorflowSpecification.get_ps_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_node_selectors) == spec.environment.tensorflow.n_ps
        assert set(tuple(i.items()) for i in ps_node_selectors.values()) == {
            tuple(spec.environment.tensorflow.default_ps_node_selectors.items()),
            tuple(spec.environment.tensorflow.ps_node_selectors[0].items())}

    def test_distributed_horovod_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/distributed_horovod_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert isinstance(spec.settings, SettingsConfig)
        assert isinstance(spec.settings.logging, LoggingConfig)
        assert spec.settings.matrix is None
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

        assert isinstance(spec.environment.horovod.worker_resources[0], PodResourcesConfig)
        assert isinstance(spec.environment.horovod.worker_resources[0].memory,
                          K8SResourcesConfig)
        assert spec.environment.horovod.worker_resources[0].index == 3
        assert spec.environment.horovod.worker_resources[0].memory.requests == 300
        assert spec.environment.horovod.worker_resources[0].memory.limits == 300

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
            spec.environment.horovod.worker_resources[0]}

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
        assert isinstance(spec.settings, SettingsConfig)
        assert isinstance(spec.settings.logging, LoggingConfig)
        assert spec.settings.matrix is None
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
        assert spec.environment.node_selectors == {'polyaxon.com': 'node_for_master_task'}
        assert spec.master_node_selectors == {'polyaxon.com': 'node_for_master_task'}
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

        assert isinstance(spec.environment.horovod.worker_resources[0], PodResourcesConfig)
        assert isinstance(spec.environment.horovod.worker_resources[0].memory,
                          K8SResourcesConfig)
        assert spec.environment.horovod.worker_resources[0].index == 3
        assert spec.environment.horovod.worker_resources[0].memory.requests == 300
        assert spec.environment.horovod.worker_resources[0].memory.limits == 300

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
            spec.environment.horovod.worker_resources[0]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4, 'limits': 2 + 3 * 4},
            'memory': {'requests': 300 + 256 * 4, 'limits': 300 + 256 * 4},
            'gpu': None
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5}, True)

        assert (spec.environment.horovod.default_worker_node_selectors ==
                {'polyaxon.com': 'node_for_worker_tasks'})
        assert (spec.environment.horovod.worker_node_selectors[0] ==
                {'index': 2, 'polyaxon.com': 'node_for_worker_task_2'})

        worker_node_selectors = HorovodSpecification.get_worker_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_node_selectors) == spec.environment.horovod.n_workers
        assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
            tuple(spec.environment.horovod.default_worker_node_selectors.items()),
            tuple(spec.environment.horovod.worker_node_selectors[0].items())}

    def test_distributed_pytorch_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/distributed_pytorch_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert isinstance(spec.settings, SettingsConfig)
        assert isinstance(spec.settings.logging, LoggingConfig)
        assert spec.settings.matrix is None
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
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

        assert isinstance(spec.environment.pytorch.worker_resources[0], PodResourcesConfig)
        assert isinstance(spec.environment.pytorch.worker_resources[0].memory,
                          K8SResourcesConfig)
        assert spec.environment.pytorch.worker_resources[0].index == 3
        assert spec.environment.pytorch.worker_resources[0].memory.requests == 300
        assert spec.environment.pytorch.worker_resources[0].memory.limits == 300

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
            spec.environment.pytorch.worker_resources[0]}

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
        assert isinstance(spec.settings, SettingsConfig)
        assert isinstance(spec.settings.logging, LoggingConfig)
        assert spec.settings.matrix is None
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
        assert spec.environment.node_selectors == {'polyaxon.com': 'node_for_master_task'}
        assert spec.master_node_selectors == {'polyaxon.com': 'node_for_master_task'}
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

        assert isinstance(spec.environment.pytorch.worker_resources[0], PodResourcesConfig)
        assert isinstance(spec.environment.pytorch.worker_resources[0].memory,
                          K8SResourcesConfig)
        assert spec.environment.pytorch.worker_resources[0].index == 3
        assert spec.environment.pytorch.worker_resources[0].memory.requests == 300
        assert spec.environment.pytorch.worker_resources[0].memory.limits == 300

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
            spec.environment.pytorch.worker_resources[0]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4, 'limits': 2 + 3 * 4},
            'memory': {'requests': 300 + 256 * 4, 'limits': 300 + 256 * 4},
            'gpu': None
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5}, True)

        assert (spec.environment.pytorch.default_worker_node_selectors ==
                {'polyaxon.com': 'node_for_worker_tasks'})
        assert (spec.environment.pytorch.worker_node_selectors[0] ==
                {'index': 2, 'polyaxon.com': 'node_for_worker_task_2'})

        worker_node_selectors = PytorchSpecification.get_worker_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_node_selectors) == spec.environment.pytorch.n_workers
        assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
            tuple(spec.environment.pytorch.default_worker_node_selectors.items()),
            tuple(spec.environment.pytorch.worker_node_selectors[0].items())}

    def test_distributed_mxnet_passes(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/distributed_mxnet_file.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert isinstance(spec.settings, SettingsConfig)
        assert isinstance(spec.settings.logging, LoggingConfig)
        assert spec.settings.matrix is None
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
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

        assert isinstance(spec.environment.mxnet.worker_resources[0], PodResourcesConfig)
        assert isinstance(spec.environment.mxnet.worker_resources[0].memory,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.worker_resources[0].index == 3
        assert spec.environment.mxnet.worker_resources[0].memory.requests == 300
        assert spec.environment.mxnet.worker_resources[0].memory.limits == 300

        assert isinstance(spec.environment.mxnet.default_ps_resources,
                          PodResourcesConfig)
        assert isinstance(spec.environment.mxnet.default_ps_resources.cpu,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.default_ps_resources.cpu.requests == 2
        assert spec.environment.mxnet.default_ps_resources.cpu.limits == 4

        assert isinstance(spec.environment.mxnet.ps_resources[0],
                          PodResourcesConfig)
        assert isinstance(spec.environment.mxnet.ps_resources[0].memory,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.ps_resources[0].index == 9
        assert spec.environment.mxnet.ps_resources[0].memory.requests == 512
        assert spec.environment.mxnet.ps_resources[0].memory.limits == 1024

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
            spec.environment.mxnet.worker_resources[0]}

        ps_resources = MXNetSpecification.get_ps_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_resources) == spec.environment.mxnet.n_ps
        assert set(ps_resources.values()) == {
            spec.environment.mxnet.default_ps_resources,
            spec.environment.mxnet.ps_resources[0]}

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
        assert isinstance(spec.settings, SettingsConfig)
        assert isinstance(spec.settings.logging, LoggingConfig)
        assert spec.settings.matrix is None
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.is_runnable
        assert spec.environment.node_selectors == {'polyaxon.com': 'node_for_master_task'}
        assert spec.master_node_selectors == {'polyaxon.com': 'node_for_master_task'}
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

        assert isinstance(spec.environment.mxnet.worker_resources[0], PodResourcesConfig)
        assert isinstance(spec.environment.mxnet.worker_resources[0].memory,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.worker_resources[0].index == 3
        assert spec.environment.mxnet.worker_resources[0].memory.requests == 300
        assert spec.environment.mxnet.worker_resources[0].memory.limits == 300

        assert isinstance(spec.environment.mxnet.default_ps_resources,
                          PodResourcesConfig)
        assert isinstance(spec.environment.mxnet.default_ps_resources.cpu,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.default_ps_resources.cpu.requests == 2
        assert spec.environment.mxnet.default_ps_resources.cpu.limits == 4

        assert isinstance(spec.environment.mxnet.ps_resources[0],
                          PodResourcesConfig)
        assert isinstance(spec.environment.mxnet.ps_resources[0].memory,
                          K8SResourcesConfig)
        assert spec.environment.mxnet.ps_resources[0].index == 9
        assert spec.environment.mxnet.ps_resources[0].memory.requests == 512
        assert spec.environment.mxnet.ps_resources[0].memory.limits == 1024

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
            spec.environment.mxnet.worker_resources[0]}

        ps_resources = MXNetSpecification.get_ps_resources(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_resources) == spec.environment.mxnet.n_ps
        assert set(ps_resources.values()) == {
            spec.environment.mxnet.default_ps_resources,
            spec.environment.mxnet.ps_resources[0]}

        # Check total resources
        assert spec.total_resources == {
            'cpu': {'requests': 1 + 3 * 4 + 2 * 9, 'limits': 2 + 3 * 4 + 4 * 9},
            'memory': {'requests': 300 + 256 * 4 + 512, 'limits': 300 + 256 * 4 + 1024},
            'gpu': None
        }

        assert spec.cluster_def == ({TaskType.MASTER: 1,
                                     TaskType.WORKER: 5,
                                     TaskType.SERVER: 10}, True)

        assert (spec.environment.mxnet.default_worker_node_selectors ==
                {'polyaxon.com': 'node_for_worker_tasks'})
        assert (spec.environment.mxnet.worker_node_selectors[0] ==
                {'index': 2, 'polyaxon.com': 'node_for_worker_task_2'})

        assert (spec.environment.mxnet.default_ps_node_selectors ==
                {'polyaxon.com': 'node_for_ps_tasks'})
        assert (spec.environment.mxnet.ps_node_selectors[0] ==
                {'index': 2, 'polyaxon.com': 'node_for_ps_task_2'})

        worker_node_selectors = MXNetSpecification.get_worker_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(worker_node_selectors) == spec.environment.mxnet.n_workers
        assert set(tuple(i.items()) for i in worker_node_selectors.values()) == {
            tuple(spec.environment.mxnet.default_worker_node_selectors.items()),
            tuple(spec.environment.mxnet.worker_node_selectors[0].items())}

        ps_node_selectors = MXNetSpecification.get_ps_node_selectors(
            environment=spec.environment,
            cluster=cluster,
            is_distributed=is_distributed
        )
        assert len(ps_node_selectors) == spec.environment.mxnet.n_ps
        assert set(tuple(i.items()) for i in ps_node_selectors.values()) == {
            tuple(spec.environment.mxnet.default_ps_node_selectors.items()),
            tuple(spec.environment.mxnet.ps_node_selectors[0].items())}

    def test_plugin_job_with_node_selectors(self):
        plxfile = PolyaxonFile(os.path.abspath(
            'tests/fixtures/plugin_with_node_selector.yml'))
        spec = plxfile.specification
        assert spec.version == 1
        assert spec.settings is None
        assert isinstance(spec.environment, EnvironmentConfig)
        assert spec.environment.node_selectors == {'polyaxon.com': 'node_for_plugin_jobs'}
        assert spec.node_selectors == {'polyaxon.com': 'node_for_plugin_jobs'}
