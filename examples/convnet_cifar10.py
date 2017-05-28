# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

import polyaxon as plx
from polyaxon.datasets import cifar10


def create_experiment_json_fn(output_dir):
    dataset_dir = './data/cifar10'
    cifar10.prepare(dataset_dir)
    train_data_file = cifar10.RECORD_FILE_NAME_FORMAT.format(dataset_dir, plx.ModeKeys.TRAIN)
    eval_data_file = cifar10.RECORD_FILE_NAME_FORMAT.format(dataset_dir, plx.ModeKeys.EVAL)
    meta_data_file = cifar10.MEAT_DATA_FILENAME_FORMAT.format(dataset_dir)

    config = {
        'name': 'real_mnsit',
        'output_dir': output_dir,
        'eval_every_n_steps': 100,
        'run_config': {'save_checkpoints_steps': 100},
        'train_input_data_config': {
            'pipeline_config': {'name': 'TFRecordImagePipeline', 'batch_size': 64,
                                'shuffle': True, 'dynamic_pad': False,
                                'params': {'data_files': train_data_file,
                                           'meta_data_file': meta_data_file}},
        },
        'eval_input_data_config': {
            'pipeline_config': {'name': 'TFRecordImagePipeline', 'batch_size': 32,
                                'shuffle': True, 'dynamic_pad': False,
                                'params': {'data_files': eval_data_file,
                                           'meta_data_file': meta_data_file}},
        },
        'estimator_config': {'output_dir': output_dir},
        'model_config': {
            'model_type': 'classifier',
            'loss_config': {'name': 'sigmoid_cross_entropy'},
            'eval_metrics_config': [{'name': 'streaming_accuracy'}],
            'optimizer_config': {'name': 'Adam', 'learning_rate': 0.001},
            'params': {'one_hot_encode': True, 'n_classes': 10},
            'graph_config': {
                'name': 'mnist',
                'features': ['image'],
                'definition': [
                    (plx.layers.Conv2d,
                     {'num_filter': 32, 'filter_size': 3, 'strides': 1, 'activation': 'relu'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2}),
                    (plx.layers.LocalResponseNormalization, {}),
                    (plx.layers.Conv2d, {'num_filter': 64, 'filter_size': 3, 'activation': 'relu'}),
                    (plx.layers.Conv2d, {'num_filter': 64, 'filter_size': 3, 'activation': 'relu'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2}),
                    (plx.layers.LocalResponseNormalization, {}),
                    (plx.layers.FullyConnected, {'n_units': 512, 'activation': 'relu'}),
                    (plx.layers.Dropout, {'keep_prob': 0.5}),
                    (plx.layers.FullyConnected, {'n_units': 10}),
                ]
            }
        }
    }
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=create_experiment_json_fn,
                                   output_dir="/tmp/polyaxon_logs/convnet_cifar10",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
