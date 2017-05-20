# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx

from examples.mnist_data import load_mnist


def create_experiment_json_fn(output_dir):
    X_train, Y_train, X_test, Y_test = load_mnist()

    config = {
        'name': 'real_mnsit',
        'output_dir': output_dir,
        'eval_every_n_steps': 5,
        'run_config': {'save_checkpoints_steps': 100},
        'train_input_data_config': {
            'input_type': plx.configs.InputDataConfig.NUMPY,
            'pipeline_config': {'name': 'train', 'batch_size': 64, 'num_epochs': 5,
                                'shuffle': True},
            'x': X_train,
            'y': Y_train
        },
        'eval_input_data_config': {
            'input_type': plx.configs.InputDataConfig.NUMPY,
            'pipeline_config': {'name': 'eval', 'batch_size': 32, 'num_epochs': 1,
                                'shuffle': False},
            'x': X_test,
            'y': Y_test
        },
        'estimator_config': {'output_dir': output_dir},
        'model_config': {
            'model_type': 'classifier',
            'loss_config': {'name': 'sigmoid_cross_entropy'},
            'eval_metrics_config': [{'name': 'streaming_accuracy'}],
            'optimizer_config': {'name': 'Adam', 'learning_rate': 0.01},
            'graph_config': {
                'name': 'mnist',
                'definition': [
                    (plx.layers.Conv2d,
                     {'num_filter': 32, 'filter_size': 3, 'strides': 1, 'activation': 'elu',
                      'regularizer': 'l2_regularizer'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2}),
                    (plx.layers.LocalResponseNormalization, {}),
                    (plx.layers.Conv2d, {'num_filter': 64, 'filter_size': 3, 'activation': 'relu',
                                         'regularizer': 'l2_regularizer'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2}),
                    (plx.layers.LocalResponseNormalization, {}),
                    (plx.layers.FullyConnected, {'n_units': 128, 'activation': 'tanh'}),
                    (plx.layers.Dropout, {'keep_prob': 0.8}),
                    (plx.layers.FullyConnected, {'n_units': 256, 'activation': 'tanh'}),
                    (plx.layers.Dropout, {'keep_prob': 0.8}),
                    (plx.layers.FullyConnected, {'n_units': 10}),
                ]
            }
        }
    }
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=create_experiment_json_fn,
                                   output_dir="/tmp/polyaxon_logs/alexnet",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
