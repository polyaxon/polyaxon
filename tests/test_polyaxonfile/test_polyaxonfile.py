# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
from unittest import TestCase

from polyaxon_schemas.exec import ExecConfig
from polyaxon_schemas.exceptions import PolyaxonfileError
from polyaxon_schemas.graph import GraphConfig
from polyaxon_schemas.k8s.templates import constants
from polyaxon_schemas.k8s.templates.persistent_volumes import get_vol_path
from polyaxon_schemas.logging import LoggingConfig
from polyaxon_schemas.losses import MeanSquaredErrorConfig, AbsoluteDifferenceConfig
from polyaxon_schemas.matrix import MatrixConfig
from polyaxon_schemas.models import ClassifierConfig, RegressorConfig
from polyaxon_schemas.optimizers import AdamConfig
from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile
from polyaxon_schemas.processing.pipelines import TFRecordImagePipelineConfig
from polyaxon_schemas.settings import (
    RunTypes,
    SettingsConfig,
    EnvironmentConfig,
    RunConfig,
    SessionConfig,
)
from polyaxon_schemas.utils import TaskType
from tests.utils import assert_equal_dict


class TestPolyaxonfile(TestCase):
    def test_missing_version_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/missing_version.yml'))

    def test_missing_project_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/missing_project.yml'))

    def test_simple_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/simple_file.yml'))
        assert plxfile.version == 1
        assert plxfile.project.name == 'project1'
        assert plxfile.project_path == '/tmp/plx_logs/project1'
        assert plxfile.matrix is None
        assert plxfile.settings is None
        assert plxfile.environment is None
        assert plxfile.run_type == RunTypes.LOCAL
        assert plxfile.cluster_def == ({TaskType.MASTER: 1}, False)
        assert_equal_dict(plxfile.get_cluster().to_dict(), {TaskType.MASTER: ['127.0.0.1:10000'],
                                                            TaskType.PS: [],
                                                            TaskType.WORKER: []})
        assert isinstance(plxfile.model, RegressorConfig)
        assert isinstance(plxfile.model.loss, MeanSquaredErrorConfig)
        assert isinstance(plxfile.model.optimizer, AdamConfig)
        assert isinstance(plxfile.model.graph, GraphConfig)
        assert len(plxfile.model.graph.layers) == 4
        assert plxfile.model.graph.input_layers == [['images', 0, 0]]
        last_layer = plxfile.model.graph.layers[-1].name
        assert plxfile.model.graph.output_layers == [[last_layer, 0, 0]]
        assert isinstance(plxfile.train.data_pipeline, TFRecordImagePipelineConfig)
        assert plxfile.eval is None

    def test_advanced_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/advanced_file.yml'))
        assert plxfile.version == 1
        assert plxfile.project.name == 'project1'
        assert plxfile.project_path == '/mypath/project1'
        assert plxfile.matrix is None
        assert plxfile.run_type == RunTypes.MINIKUBE
        assert isinstance(plxfile.settings, SettingsConfig)
        assert isinstance(plxfile.settings.logging, LoggingConfig)
        assert isinstance(plxfile.environment, EnvironmentConfig)
        assert plxfile.environment.n_workers == 5
        assert plxfile.environment.n_ps == 10
        assert plxfile.environment.delay_workers_by_global_step is True
        assert isinstance(plxfile.environment.run_config, RunConfig)
        assert plxfile.environment.run_config.tf_random_seed == 100
        assert plxfile.environment.run_config.save_summary_steps == 100
        assert plxfile.environment.run_config.save_checkpoints_secs == 60
        assert isinstance(plxfile.environment.run_config.session, SessionConfig)
        assert plxfile.environment.run_config.session.allow_soft_placement is True
        assert plxfile.environment.run_config.session.intra_op_parallelism_threads == 2
        assert plxfile.environment.run_config.session.inter_op_parallelism_threads == 2

        assert plxfile.cluster_def == ({TaskType.MASTER: 1,
                                        TaskType.WORKER: 5,
                                        TaskType.PS: 10}, True)

        def task_name(task_type, task_id):
            return constants.TASK_NAME.format(project=plxfile.project.name,
                                              experiment=0,
                                              task_type=task_type,
                                              task_id=task_id)

        assert_equal_dict(plxfile.get_cluster().to_dict(),
                          {TaskType.MASTER: ['{}:2222'.format(task_name(TaskType.MASTER, 0))],
                           TaskType.WORKER: [
                               '{}:2222'.format(task_name(TaskType.WORKER, 0)),
                               '{}:2222'.format(task_name(TaskType.WORKER, 1)),
                               '{}:2222'.format(task_name(TaskType.WORKER, 2)),
                               '{}:2222'.format(task_name(TaskType.WORKER, 3)),
                               '{}:2222'.format(task_name(TaskType.WORKER, 4)),
                           ],
                           TaskType.PS: [
                               '{}:2222'.format(task_name(TaskType.PS, 0)),
                               '{}:2222'.format(task_name(TaskType.PS, 1)),
                               '{}:2222'.format(task_name(TaskType.PS, 2)),
                               '{}:2222'.format(task_name(TaskType.PS, 3)),
                               '{}:2222'.format(task_name(TaskType.PS, 4)),
                               '{}:2222'.format(task_name(TaskType.PS, 5)),
                               '{}:2222'.format(task_name(TaskType.PS, 6)),
                               '{}:2222'.format(task_name(TaskType.PS, 7)),
                               '{}:2222'.format(task_name(TaskType.PS, 8)),
                               '{}:2222'.format(task_name(TaskType.PS, 9)),
                           ]})
        assert isinstance(plxfile.model, ClassifierConfig)
        assert isinstance(plxfile.model.loss, MeanSquaredErrorConfig)
        assert isinstance(plxfile.model.optimizer, AdamConfig)
        assert plxfile.model.optimizer.learning_rate == 0.21
        assert isinstance(plxfile.model.graph, GraphConfig)
        assert len(plxfile.model.graph.layers) == 7
        assert plxfile.model.graph.input_layers == [['images', 0, 0]]
        assert len(plxfile.model.graph.output_layers) == 3
        assert ['super_dense', 0, 0] in plxfile.model.graph.output_layers
        assert isinstance(plxfile.train.data_pipeline, TFRecordImagePipelineConfig)
        assert len(plxfile.train.data_pipeline.feature_processors.feature_processors) == 1
        assert isinstance(plxfile.eval.data_pipeline, TFRecordImagePipelineConfig)
        assert plxfile.eval.data_pipeline.feature_processors is None

    def test_matrix_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/matrix_file.yml'))
        assert plxfile.version == 1
        assert plxfile.project.name == 'project1'
        assert plxfile.project_path == '/tmp/plx_logs/project1'
        assert isinstance(plxfile.matrix['lr'], MatrixConfig)
        assert isinstance(plxfile.matrix['loss'], MatrixConfig)
        assert plxfile.matrix['lr'].to_dict() == {
            'logspace': {'start': 0.01, 'stop': 0.1, 'num': 5}}
        assert plxfile.matrix['loss'].to_dict() == {'values': ['MeanSquaredError',
                                                               'AbsoluteDifference']}
        assert plxfile.matrix_space == 10
        declarations = []
        for lr in plxfile.matrix['lr'].to_numpy():
            for loss in plxfile.matrix['loss'].to_numpy():
                declarations.append({'loss': loss, 'lr': lr})
        assert sorted(
            plxfile.matrix_declarations, key=lambda x: (x['lr'], x['loss'])) == sorted(
            declarations, key=lambda x: (x['lr'], x['loss']))
        assert plxfile.settings is None
        assert plxfile.run_type == RunTypes.LOCAL
        # we cannot access property because the current polyaxonfile has multiple experiments
        with self.assertRaises(AttributeError):
            plxfile.environment
        with self.assertRaises(AttributeError):
            plxfile.cluster_def
        with self.assertRaises(AttributeError):
            plxfile.model
        with self.assertRaises(AttributeError):
            plxfile.train

        for xp in range(plxfile.matrix_space):
            assert plxfile.get_environment_at(xp) is None
            assert plxfile.get_cluster_def_at(xp) == ({TaskType.MASTER: 1}, False)

            assert_equal_dict(plxfile.get_cluster(xp).to_dict(),
                              {TaskType.MASTER: ['127.0.0.1:10000'],
                               TaskType.PS: [],
                               TaskType.WORKER: []})
            model = plxfile.get_model_at(xp)
            assert isinstance(model, RegressorConfig)
            assert isinstance(model.loss, (MeanSquaredErrorConfig, AbsoluteDifferenceConfig))
            assert isinstance(model.optimizer, AdamConfig)
            assert isinstance(model.graph, GraphConfig)
            assert len(model.graph.layers) == 4
            assert model.graph.input_layers == [['images', 0, 0]]
            last_layer = model.graph.layers[-1].name
            assert model.graph.output_layers == [[last_layer, 0, 0]]
            assert isinstance(plxfile.get_train_at(xp).data_pipeline, TFRecordImagePipelineConfig)

    def test_one_matrix_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/one_matrix_file.yml'))
        assert plxfile.version == 1
        assert plxfile.project.name == 'project1'
        assert plxfile.project_path == '/tmp/plx_logs/project1'
        assert isinstance(plxfile.matrix['loss'], MatrixConfig)
        assert plxfile.matrix['loss'].to_dict() == {'values': ['MeanSquaredError',
                                                               'AbsoluteDifference']}
        assert plxfile.matrix_space == 2
        declarations = []
        for loss in plxfile.matrix['loss'].to_numpy():
            declarations.append({'loss': loss})
        assert sorted(
            plxfile.matrix_declarations, key=lambda x: (x['loss'])) == sorted(
            declarations, key=lambda x: (x['loss']))
        assert plxfile.settings is None
        assert plxfile.run_type == RunTypes.LOCAL
        # we cannot access property because the current polyaxonfile has multiple experiments
        with self.assertRaises(AttributeError):
            plxfile.environment
        with self.assertRaises(AttributeError):
            plxfile.cluster_def
        with self.assertRaises(AttributeError):
            plxfile.model
        with self.assertRaises(AttributeError):
            plxfile.train

        for xp in range(plxfile.matrix_space):
            assert plxfile.get_environment_at(xp) is None
            assert plxfile.get_cluster_def_at(xp) == ({TaskType.MASTER: 1}, False)

            assert_equal_dict(plxfile.get_cluster(xp).to_dict(),
                              {TaskType.MASTER: ['127.0.0.1:10000'],
                               TaskType.PS: [],
                               TaskType.WORKER: []})
            model = plxfile.get_model_at(xp)
            assert isinstance(model, RegressorConfig)
            assert isinstance(model.loss, (MeanSquaredErrorConfig, AbsoluteDifferenceConfig))
            assert isinstance(model.optimizer, AdamConfig)
            assert isinstance(model.graph, GraphConfig)
            assert len(model.graph.layers) == 4
            assert model.graph.input_layers == [['images', 0, 0]]
            last_layer = model.graph.layers[-1].name
            assert model.graph.output_layers == [[last_layer, 0, 0]]
            assert isinstance(plxfile.get_train_at(xp).data_pipeline, TFRecordImagePipelineConfig)

    def test_exec_simple_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/exec_simple_file.yml'))
        assert plxfile.version == 1
        assert plxfile.project.name == 'video_prediction'
        assert plxfile.project_path == "/tmp/plx_logs/video_prediction"
        assert plxfile.settings is None
        assert plxfile.run_type == RunTypes.LOCAL
        assert plxfile.environment is None
        assert plxfile.cluster_def == ({TaskType.MASTER: 1}, False)
        assert plxfile.model is None
        exec = plxfile.exec
        assert isinstance(exec, ExecConfig)
        assert exec.cmd == "video_prediction_train --model=DNA --num_masks=1"

    def test_exec_matrix_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/exec_matrix_file.yml'))
        assert plxfile.version == 1
        assert plxfile.project.name == 'video_prediction'
        assert plxfile.project_path == get_vol_path('video_prediction',
                                                    constants.LOGS_VOLUME,
                                                    RunTypes.MINIKUBE)
        assert isinstance(plxfile.matrix['model'], MatrixConfig)
        assert plxfile.matrix['model'].to_dict() == {'values': ['CDNA', 'DNA', 'STP']}
        assert plxfile.matrix_space == 3
        declarations = []
        for loss in plxfile.matrix['model'].to_numpy():
            declarations.append({'model': loss})
        assert sorted(
            plxfile.matrix_declarations, key=lambda x: (x['model'])) == sorted(
            declarations, key=lambda x: (x['model']))
        assert isinstance(plxfile.settings, SettingsConfig)
        assert plxfile.run_type == RunTypes.MINIKUBE
        # we cannot access property because the current polyaxonfile has multiple experiments
        with self.assertRaises(AttributeError):
            plxfile.environment
        with self.assertRaises(AttributeError):
            plxfile.cluster_def
        with self.assertRaises(AttributeError):
            plxfile.model
        with self.assertRaises(AttributeError):
            plxfile.train
        with self.assertRaises(AttributeError):
            plxfile.exec

        for xp in range(plxfile.matrix_space):
            assert plxfile.get_environment_at(xp) is None
            assert plxfile.get_cluster_def_at(xp) == ({TaskType.MASTER: 1}, False)
            assert plxfile.get_model_at(xp) is None
            exec = plxfile.get_exec_at(xp)
            assert isinstance(exec, ExecConfig)
            declarations = plxfile.get_declarations_at(xp)
            declarations['num_masks'] = 1 if declarations['model'] == 'DNA' else 10
            assert exec.cmd == 'video_prediction_train --model="{model}" --num_masks={num_masks}'.format(
                **declarations
            )
