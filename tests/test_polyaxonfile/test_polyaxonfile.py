# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
from unittest import TestCase

from polyaxon_schemas.exceptions import PolyaxonfileError
from polyaxon_schemas.graph import GraphConfig
from polyaxon_schemas.logging import LoggingConfig
from polyaxon_schemas.losses import MeanSquaredErrorConfig
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
from tests.utils import assert_equal_dict


class TestPolyaxonfile(TestCase):
    def test_missing_version_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/missing_version.yml'))

    def test_missing_model_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/missing_model.yml'))

    def test_missing_project_raises(self):
        with self.assertRaises(PolyaxonfileError):
            PolyaxonFile(os.path.abspath('tests/fixtures/missing_project.yml'))

    def test_simple_file_passes(self):
        plxfile = PolyaxonFile(os.path.abspath('tests/fixtures/simple_file.yml'))
        assert plxfile.version == 1
        assert plxfile.project.name == 'project1'
        assert plxfile.project_path == '/tmp/plx_logs/project1'
        assert plxfile.settings is None
        assert plxfile.environment is None
        assert plxfile.run_type == RunTypes.LOCAL
        assert plxfile.cluster_def == ({'master': 1}, False)
        assert_equal_dict(plxfile.get_cluster().to_dict(), {'master': ['127.0.0.1:10000'],
                                                            'ps': [],
                                                            'worker': []})
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

        assert plxfile.cluster_def == ({'master': 1, 'worker': 5, 'ps': 10}, True)
        assert_equal_dict(plxfile.get_cluster().to_dict(), {'master': ['127.0.0.1:10000'],
                                                            'worker': ['127.0.0.1:11000',
                                                                       '127.0.0.1:11001',
                                                                       '127.0.0.1:11002',
                                                                       '127.0.0.1:11003',
                                                                       '127.0.0.1:11004',
                                                                       ],
                                                            'ps': ['127.0.0.1:12000',
                                                                   '127.0.0.1:12001',
                                                                   '127.0.0.1:12002',
                                                                   '127.0.0.1:12003',
                                                                   '127.0.0.1:12004',
                                                                   '127.0.0.1:12005',
                                                                   '127.0.0.1:12006',
                                                                   '127.0.0.1:12007',
                                                                   '127.0.0.1:12008',
                                                                   '127.0.0.1:12009',
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
