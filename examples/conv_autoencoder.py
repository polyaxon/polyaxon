# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

import polyaxon as plx
from polyaxon.datasets import mnist


def create_experiment_json_fn(output_dir):
    """Creates an auto encoder on MNIST handwritten digits.

    inks:
        * [MNIST Dataset] http://yann.lecun.com/exdb/mnist/
    """
    dataset_dir = './data/mnist'
    mnist.prepare(dataset_dir)
    train_data_file = mnist.RECORD_FILE_NAME_FORMAT.format(dataset_dir, plx.Modes.TRAIN)
    eval_data_file = mnist.RECORD_FILE_NAME_FORMAT.format(dataset_dir, plx.Modes.EVAL)
    meta_data_file = mnist.MEAT_DATA_FILENAME_FORMAT.format(dataset_dir)

    config = {
        'name': 'conv_autoencoder_mnsit',
        'output_dir': output_dir,
        'eval_every_n_steps': 100,
        'train_steps_per_iteration': 1000,
        'run_config': {'save_checkpoints_steps': 1000},
        'train_input_data_config': {
            'pipeline_config': {'module': 'TFRecordImagePipeline', 'batch_size': 64,  'num_epochs': 10,
                                'shuffle': True, 'dynamic_pad': False,
                                'params': {'data_files': train_data_file,
                                           'meta_data_file': meta_data_file},
                                'definition': {
                                    'image': [
                                        (plx.processing.image.Standardization, {}),
                                    ]
                                }
                                },
        },
        'eval_input_data_config': {
            'pipeline_config': {'module': 'TFRecordImagePipeline', 'batch_size': 32,  'num_epochs': 1,
                                'shuffle': True, 'dynamic_pad': False,
                                'params': {'data_files': eval_data_file,
                                           'meta_data_file': meta_data_file},
                                'definition': {
                                    'image': [
                                        (plx.processing.image.Standardization, {}),
                                    ]
                                }
                                },
        },
        'estimator_config': {'output_dir': output_dir},
        'model_config': {
            'summaries': ['loss', 'image_input', 'image_result', 'image_generated'],
            'module': 'Generator',
            'optimizer_config': {'module': 'adadelta', 'learning_rate': 0.9},
            'encoder_config': {
                'definition': [
                    (plx.layers.Conv2d,
                     {'num_filter': 32, 'filter_size': 3, 'strides': 1, 'activation': 'relu',
                      'regularizer': 'l2_regularizer'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2}),
                    (plx.layers.Conv2d, {'num_filter': 32, 'filter_size': 3, 'activation': 'relu',
                                         'regularizer': 'l2_regularizer'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2}),
                ]
            },
            'decoder_config': {
                'definition': [
                    (plx.layers.Conv2d,
                     {'num_filter': 32, 'filter_size': 3, 'strides': 1, 'activation': 'relu',
                      'regularizer': 'l2_regularizer'}),
                    (plx.layers.Upsample2d, {'kernel_size': 2}),
                    (plx.layers.Conv2d, {'num_filter': 32, 'filter_size': 3, 'activation': 'relu',
                                         'regularizer': 'l2_regularizer'}),
                    (plx.layers.Upsample2d, {'kernel_size': 2}),
                    (plx.layers.Conv2d, {'num_filter': 1, 'filter_size': 3, 'activation': 'relu',
                                         'regularizer': 'l2_regularizer'}),
                ]
            }
        }
    }
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=create_experiment_json_fn,
                                   output_dir="/tmp/polyaxon_logs/conv_autoencoder",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
