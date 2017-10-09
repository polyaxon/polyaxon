# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.test import TestCase

import polyaxon as plx

from experiments.models import Experiment, Loss, Optimizer, SubGraph, PolyaxonModel


class TestCoreModels(TestCase):
    def test_read_from_to_configs(self):
        config = {
            'name': 'conv_mnsit',
            'output_dir': 'output_dir',
            'eval_every_n_steps': 5,
            'run_config': {'save_checkpoints_steps': 100},
            'train_input_data_config': {
                'pipeline_config': {'module': 'TFRecordImagePipeline', 'batch_size': 64,
                                    'num_epochs': 5,
                                    'shuffle': True, 'dynamic_pad': False,
                                    'params': {'data_files': 'train_data_file',
                                               'meta_data_file': 'meta_data_file'}},
            },
            'eval_input_data_config': {
                'pipeline_config': {'module': 'TFRecordImagePipeline', 'batch_size': 32,
                                    'num_epochs': 1,
                                    'shuffle': True, 'dynamic_pad': False,
                                    'params': {'data_files': 'eval_data_file',
                                               'meta_data_file': 'meta_data_file'}},
            },
            'estimator_config': {'output_dir': 'output_dir'},
            'model_config': {
                'module': 'Classifier',
                'loss_config': {'module': 'sigmoid_cross_entropy'},
                'eval_metrics_config': [{'module': 'streaming_accuracy'}],
                'optimizer_config': {'module': 'adam', 'learning_rate': 0.001},
                'one_hot_encode': True,
                'n_classes': 10,
                'graph_config': {
                    'name': 'convnet',
                    'features': ['image'],
                    'definition': [
                        ('Conv2d',
                         {'num_filter': 32, 'filter_size': 3, 'strides': 1, 'activation': 'elu',
                          'regularizer': 'l2_regularizer'}),
                        ('MaxPool2d', {'kernel_size': 2}),
                        ('LocalResponseNormalization', {}),
                        ('Conv2d', {'num_filter': 64, 'filter_size': 3, 'activation': 'relu',
                                    'regularizer': 'l2_regularizer'}),
                        ('MaxPool2d', {'kernel_size': 2}),
                        ('LocalResponseNormalization', {}),
                        ('FullyConnected', {'num_units': 128, 'activation': 'tanh'}),
                        ('Dropout', {'keep_prob': 0.8}),
                        ('FullyConnected', {'num_units': 256, 'activation': 'tanh'}),
                        ('Dropout', {'keep_prob': 0.8}),
                        ('FullyConnected', {'num_units': 10}),
                    ]
                }
            }
        }
        experiment_config = plx.configs.ExperimentConfig.read_configs(config)
        experiment = Experiment.from_config(experiment_config)
        assert isinstance(experiment, Experiment)
        assert isinstance(experiment.model, PolyaxonModel)
        assert isinstance(experiment.model.graph, SubGraph)
        assert isinstance(experiment.model.loss, Loss)
        assert isinstance(experiment.model.optimizer, Optimizer)

        experiment_dict = experiment.to_dict()
        assert isinstance(experiment_dict, dict)

        experiment_config_result = experiment.to_config()
        assert isinstance(experiment_config_result, plx.configs.ExperimentConfig)

        # re import the config should work
        experiment = Experiment.from_config(experiment_config_result)
        assert isinstance(experiment, Experiment)

        # read from db
        experiment = Experiment.objects.all()[0]
        experiment_dict = experiment.to_dict()
        assert isinstance(experiment_dict, dict)
        experiment_config_result = experiment.to_config()
        assert isinstance(experiment_config_result, plx.configs.ExperimentConfig)
        experiment = Experiment.from_config(experiment_config_result)
        assert isinstance(experiment, Experiment)
