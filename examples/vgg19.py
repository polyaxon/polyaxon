# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

import polyaxon as plx
from polyaxon.datasets import mnist


def create_experiment_json_fn(output_dir):
    """Creates an experiement using a VGG19 to Oxford's 17 Category Flower Dataset.

    References:
        * Very Deep Convolutional Networks for Large-Scale Image Recognition.
        K. Simonyan, A. Zisserman. arXiv technical report, 2014.

    Links:
        * http://arxiv.org/pdf/1409.1556
    """
    dataset_dir = './data/mnist'
    mnist.prepare(dataset_dir)
    train_data_file = mnist.RECORD_FILE_NAME_FORMAT.format(dataset_dir, plx.Modes.TRAIN)
    eval_data_file = mnist.RECORD_FILE_NAME_FORMAT.format(dataset_dir, plx.Modes.EVAL)
    meta_data_file = mnist.MEAT_DATA_FILENAME_FORMAT.format(dataset_dir)

    config = {
        'name': 'vgg19',
        'output_dir': output_dir,
        'eval_every_n_steps': 10,
        'train_steps_per_iteration': 100,
        'run_config': {'save_checkpoints_steps': 100},
        'train_input_data_config': {
            'pipeline_config': {'module': 'TFRecordImagePipeline', 'batch_size': 64,  'num_epochs': 1,
                                'shuffle': True, 'dynamic_pad': False,
                                'params': {'data_files': train_data_file,
                                           'meta_data_file': meta_data_file}},
        },
        'eval_input_data_config': {
            'pipeline_config': {'module': 'TFRecordImagePipeline', 'batch_size': 32,  'num_epochs': 1,
                                'shuffle': True, 'dynamic_pad': False,
                                'params': {'data_files': eval_data_file,
                                           'meta_data_file': meta_data_file}},
        },
        'estimator_config': {'output_dir': output_dir},
        'model_config': {
            'module': 'Classifier',
            'summaries': ['loss'],
            'loss_config': {'module': 'softmax_cross_entropy'},
            'eval_metrics_config': [{'module': 'streaming_accuracy'},
                                    {'module': 'streaming_precision'}],
            'optimizer_config': {'module': 'adam', 'learning_rate': 0.007,
                                 'decay_type': 'exponential_decay', 'decay_rate': 0.2},
            'one_hot_encode': True,
            'n_classes': 17,
            'graph_config': {
                'name': 'vgg',
                'features': ['image'],
                'definition': [
                    (plx.layers.Conv2d, {'num_filter': 64, 'filter_size': 3,
                                         'activation': 'relu'}),
                    (plx.layers.Conv2d, {'num_filter': 64, 'filter_size': 3,
                                         'activation': 'relu'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2, 'strides': 2}),

                    (plx.layers.Conv2d, {'num_filter': 128, 'filter_size': 3,
                                         'activation': 'relu'}),
                    (plx.layers.Conv2d, {'num_filter': 128, 'filter_size': 3,
                                         'activation': 'relu'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2, 'strides': 2}),

                    (plx.layers.Conv2d, {'num_filter': 256, 'filter_size': 3,
                                         'activation': 'relu'}),
                    (plx.layers.Conv2d, {'num_filter': 256, 'filter_size': 3,
                                         'activation': 'relu'}),
                    (plx.layers.Conv2d, {'num_filter': 256, 'filter_size': 3,
                                         'activation': 'relu'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2, 'strides': 2}),

                    (plx.layers.Conv2d, {'num_filter': 512, 'filter_size': 3,
                                         'activation': 'relu'}),
                    (plx.layers.Conv2d, {'num_filter': 512, 'filter_size': 3,
                                         'activation': 'relu'}),
                    (plx.layers.Conv2d, {'num_filter': 512, 'filter_size': 3,
                                         'activation': 'relu'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2, 'strides': 2}),

                    (plx.layers.FullyConnected, {'num_units': 4096, 'activation': 'relu',
                                                 'dropout': 0.5}),
                    (plx.layers.FullyConnected, {'num_units': 4096, 'activation': 'relu',
                                                 'dropout': 0.5}),
                    (plx.layers.FullyConnected, {'num_units': 17}),
                ]
            }
        }
    }
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=create_experiment_json_fn,
                                   output_dir="/tmp/polyaxon_logs/vgg19",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
