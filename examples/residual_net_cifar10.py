# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

import polyaxon as plx
from polyaxon.datasets import cifar10


def create_experiment_json_fn(output_dir):
    """Creates an experiment using deep residual network.

    References:
        * K. He, X. Zhang, S. Ren, and J. Sun. Deep Residual Learning for Image
          Recognition, 2015.
        * Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner. "Gradient-based
          learning applied to document recognition." Proceedings of the IEEE,
          86(11):2278-2324, November 1998.
    Links:
        * [Deep Residual Network](http://arxiv.org/pdf/1512.03385.pdf)
        * [MNIST Dataset](http://yann.lecun.com/exdb/mnist/)

    """
    dataset_dir = './data/cifar10'
    cifar10.prepare(dataset_dir)
    train_data_file = cifar10.RECORD_FILE_NAME_FORMAT.format(dataset_dir, plx.ModeKeys.TRAIN)
    eval_data_file = cifar10.RECORD_FILE_NAME_FORMAT.format(dataset_dir, plx.ModeKeys.EVAL)
    meta_data_file = cifar10.MEAT_DATA_FILENAME_FORMAT.format(dataset_dir)

    config = {
        'name': 'residual_net_cifar10',
        'output_dir': output_dir,
        'eval_every_n_steps': 10,
        'train_steps_per_iteration': 100,
        'run_config': {'save_checkpoints_steps': 100},
        'train_input_data_config': {
            'pipeline_config': {'name': 'TFRecordImagePipeline', 'batch_size': 64, 'num_epochs': 1,
                                'shuffle': True, 'dynamic_pad': False,
                                'params': {'data_files': train_data_file,
                                           'meta_data_file': meta_data_file},
                                'definition': {
                                    'image': [
                                        (plx.processing.image.Flip, {'is_random': True}),
                                        (plx.processing.image.RandomCrop, {'height': 32, 'width': 32})
                                    ]
                                }
                                },
        },
        'eval_input_data_config': {
            'pipeline_config': {'name': 'TFRecordImagePipeline', 'batch_size': 32, 'num_epochs': 1,
                                'shuffle': True, 'dynamic_pad': False,
                                'params': {'data_files': eval_data_file,
                                           'meta_data_file': meta_data_file}},
        },
        'estimator_config': {'output_dir': output_dir},
        'model_config': {
            'summaries': 'all',
            'model_type': 'classifier',
            'loss_config': {'name': 'softmax_cross_entropy'},
            'eval_metrics_config': [{'name': 'streaming_accuracy'},],
            'optimizer_config': {'name': 'Adam', 'learning_rate': 0.07,
                                 'decay_type': 'exponential_decay', 'decay_rate': 0.2},
            'one_hot_encode': True,
            'n_classes': 10,
            'graph_config': {
                'name': 'resnet',
                'features': ['image'],
                'definition': [
                    (plx.layers.Conv2d, {'num_filter': 16, 'filter_size': 3, 'strides': 1,
                                         'scale': 0.0001, 'regularizer': 'l2_regularizer'}),
                    (plx.layers.ResidualBlock, {'num_blocks': 5, 'out_channels': 16}),
                    (plx.layers.ResidualBlock, {'num_blocks': 1, 'out_channels': 32,
                                                'downsample': True}),
                    (plx.layers.ResidualBlock, {'num_blocks': 4, 'out_channels': 32}),
                    (plx.layers.ResidualBlock, {'num_blocks': 1, 'out_channels': 64,
                                                'downsample': True}),
                    (plx.layers.ResidualBlock, {'num_blocks': 4, 'out_channels': 64,
                                                'activation': 'relu'}),
                    (plx.layers.BatchNormalization, {}),
                    (plx.layers.GlobalAvgPool, {}),
                    (plx.layers.FullyConnected, {'num_units': 10})
                ]
            }
        }
    }
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=create_experiment_json_fn,
                                   output_dir="/tmp/polyaxon_logs/res_net_cifar10",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
