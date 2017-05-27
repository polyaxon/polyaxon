# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

import polyaxon as plx
from polyaxon.datasets import mnist


def create_experiment_json_fn(output_dir):
    dataset_dir = './data/mnist'
    mnist.prepare(dataset_dir)
    train_data_file = mnist.RECORD_FILE_NAME_FORMAT.format(dataset_dir, plx.ModeKeys.TRAIN)
    eval_data_file = mnist.RECORD_FILE_NAME_FORMAT.format(dataset_dir, plx.ModeKeys.EVAL)
    meta_data_file = mnist.MEAT_DATA_FILENAME.format(dataset_dir)

    config = {
        'name': 'lenet_mnsit',
        'output_dir': output_dir,
        'eval_every_n_steps': 10,
        'train_steps_per_iteration': 100,
        'run_config': {'save_checkpoints_steps': 100},
        'train_input_data_config': {
            'pipeline_config': {'name': 'TFRecordPipeline', 'batch_size': 64,  'num_epochs': 1,
                                'shuffle': True, 'dynamic_pad': False,
                                'params': {'data_files': train_data_file,
                                           'meta_data_file': meta_data_file}},
        },
        'eval_input_data_config': {
            'pipeline_config': {'name': 'TFRecordPipeline', 'batch_size': 32,  'num_epochs': 1,
                                'shuffle': True, 'dynamic_pad': False,
                                'params': {'data_files': eval_data_file,
                                           'meta_data_file': meta_data_file}},
        },
        'estimator_config': {'output_dir': output_dir},
        'model_config': {
            'summaries': 'all',
            'model_type': 'classifier',
            'loss_config': {'name': 'softmax_cross_entropy'},
            'eval_metrics_config': [{'name': 'streaming_accuracy'},
                                    {'name': 'streaming_precision'}],
            'optimizer_config': {'name': 'Adam', 'learning_rate': 0.07,
                                 'decay_type': 'exponential_decay', 'decay_rate': 0.2},
            'params': {'one_hot_encode': True, 'n_classes': 10},
            'graph_config': {
                'name': 'lenet',
                'features': ['image'],
                'definition': [
                    (plx.layers.Conv2d, {'num_filter': 32, 'filter_size': 5, 'strides': 1,
                                         'regularizer': 'l2_regularizer'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2}),
                    (plx.layers.Conv2d, {'num_filter': 64, 'filter_size': 5,
                                         'regularizer': 'l2_regularizer'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2}),
                    (plx.layers.FullyConnected, {'n_units': 1024, 'activation': 'tanh'}),
                    (plx.layers.FullyConnected, {'n_units': 10}),
                ]
            }
        }
    }
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=create_experiment_json_fn,
                                   output_dir="/tmp/polyaxon_logs/lenet",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
