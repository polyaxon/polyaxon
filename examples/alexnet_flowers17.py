# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

import polyaxon as plx
from polyaxon.datasets import flowers17


def create_experiment_json_fn(output_dir):
    """Creates an experiment using Alexnet applied to Oxford's 17  Category Flower Dataset.

    References:
        * Alex Krizhevsky, Ilya Sutskever & Geoffrey E. Hinton. ImageNet Classification with
        Deep Convolutional Neural Networks. NIPS, 2012.
        * 17 Category Flower Dataset. Maria-Elena Nilsback and Andrew Zisserman.

    Links:
        * [AlexNet Paper](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)
        * [Flower Dataset (17)](http://www.robots.ox.ac.uk/~vgg/data/flowers/17/)
    """
    dataset_dir = './data/flowers17'
    flowers17.prepare(dataset_dir)
    train_data_file = flowers17.RECORD_FILE_NAME_FORMAT.format(dataset_dir, plx.ModeKeys.TRAIN)
    eval_data_file = flowers17.RECORD_FILE_NAME_FORMAT.format(dataset_dir, plx.ModeKeys.EVAL)
    meta_data_file = flowers17.MEAT_DATA_FILENAME_FORMAT.format(dataset_dir)

    config = {
        'name': 'alexnet_flowers17',
        'output_dir': output_dir,
        'eval_every_n_steps': 10,
        'train_steps_per_iteration': 100,
        'run_config': {'save_checkpoints_steps': 100},
        'train_input_data_config': {
            'pipeline_config': {'name': 'TFRecordImagePipeline', 'batch_size': 64, 'num_epochs': 1,
                                'shuffle': True, 'dynamic_pad': False,
                                'params': {'data_files': train_data_file,
                                           'meta_data_file': meta_data_file}},
        },
        'eval_input_data_config': {
            'pipeline_config': {'name': 'TFRecordImagePipeline', 'batch_size': 32, 'num_epochs': 1,
                                'shuffle': True, 'dynamic_pad': False,
                                'params': {'data_files': eval_data_file,
                                           'meta_data_file': meta_data_file}},
        },
        'estimator_config': {'output_dir': output_dir},
        'model_config': {
            'model_type': 'classifier',
            'summaries': ['loss'],
            'loss_config': {'name': 'sigmoid_cross_entropy'},
            'eval_metrics_config': [{'name': 'streaming_accuracy'}],
            'optimizer_config': {'name': 'Momentum', 'learning_rate': 0.001},
            'params': {'one_hot_encode': True, 'n_classes': 17},
            'graph_config': {
                'name': 'alextnet',
                'features': ['image'],
                'definition': [
                    (plx.layers.Conv2d,
                     {'num_filter': 96, 'filter_size': 11, 'strides': 4, 'activation': 'relu',
                      'regularizer': 'l2_regularizer'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 3, 'strides': 2}),
                    (plx.layers.LocalResponseNormalization, {}),
                    (plx.layers.Conv2d, {'num_filter': 156, 'filter_size': 5, 'activation': 'relu',
                                         'regularizer': 'l2_regularizer'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 3, 'strides': 2}),
                    (plx.layers.LocalResponseNormalization, {}),
                    (plx.layers.Conv2d,
                     {'num_filter': 384, 'filter_size': 3, 'activation': 'relu'}),
                    (plx.layers.Conv2d,
                     {'num_filter': 384, 'filter_size': 3, 'activation': 'relu'}),
                    (plx.layers.Conv2d,
                     {'num_filter': 256, 'filter_size': 3, 'activation': 'relu'}),
                    (plx.layers.MaxPool2d,
                     {'kernel_size': 3, 'strides': 2}),
                    (plx.layers.LocalResponseNormalization, {}),
                    (plx.layers.FullyConnected,
                     {'num_units': 4096, 'activation': 'tanh', 'keep_prob': 0.5}),
                    (plx.layers.FullyConnected, {'num_units': 4096, 'activation': 'tanh'}),
                    (plx.layers.Dropout, {'keep_prob': 0.5}),
                    (plx.layers.FullyConnected, {'num_units': 17}),
                ]
            }
        }
    }
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=create_experiment_json_fn,
                                   output_dir="/tmp/polyaxon_logs/alexnet_flowers17",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
