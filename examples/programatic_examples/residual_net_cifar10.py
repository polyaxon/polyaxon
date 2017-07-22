# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

import polyaxon as plx


def graph_fn(mode, inputs):
    x = plx.layers.Conv2d(
        mode=mode, num_filter=16, filter_size=2, strides=1, scale=0.0001, 
        regularizer='l2_regularizer')(inputs['image'])
    x = plx.layers.ResidualBlock(mode=mode, num_blocks=5, out_channels=16)(x)
    x = plx.layers.ResidualBlock(mode=mode, num_blocks=1, out_channels=32, downsample=True)(x)
    x = plx.layers.ResidualBlock(mode=mode, num_blocks=4, out_channels=32)(x)
    x = plx.layers.ResidualBlock(mode=mode, num_blocks=1, out_channels=64, downsample=True)(x)
    x = plx.layers.ResidualBlock(mode=mode, num_blocks=4, out_channels=64, activation='relu')(x)
    x = plx.layers.LocalResponseNormalization(mode=mode)(x)
    x = plx.layers.GlobalAvgPool(mode=mode)(x)
    x = plx.layers.FullyConnected(mode=mode, num_units=10)(x)
    return x


def model_fn(features, labels, params, mode, config):
    model = plx.models.Classifier(
        mode=mode,
        graph_fn=graph_fn,
        loss_config=plx.configs.LossConfig(module='softmax_cross_entropy'),
        optimizer_config=plx.configs.OptimizerConfig(
            module='adam', learning_rate=0.001, decay_type='exponential_decay', decay_rate=0.2),
        eval_metrics_config=[plx.configs.MetricConfig(module='streaming_accuracy')],
        summaries=['loss'],
        one_hot_encode=True,
        n_classes=10)
    return model(features=features, labels=labels, params=params, config=config)


def get_train_input_fn(data_files, meta_data_file):
    config = plx.configs.InputDataConfig.read_configs(
        {
            "pipeline_config": {
                "module": "TFRecordImagePipeline",
                "batch_size": 64,
                "num_epochs": 1,
                "shuffle": True,
                "dynamic_pad": False,
                "params": {
                    "data_files": data_files,
                    "meta_data_file": meta_data_file
                },
                "definition": {
                    "image": [
                        ["Flip", {'is_random': True}],
                        ["RandomCrop", {'height': 32, 'width': 32}]
                    ]
                }
            }
        }
    )

    return plx.processing.create_input_data_fn(mode=plx.Modes.TRAIN,
                                               pipeline_config=config.pipeline_config)


def get_eval_input_fn(data_files, meta_data_file):
    config = plx.configs.InputDataConfig.read_configs(
        {
            "pipeline_config": {
                "module": "TFRecordImagePipeline",
                "batch_size": 32,
                "num_epochs": 1,
                "shuffle": True,
                "dynamic_pad": False,
                "params": {
                    "data_files": data_files,
                    "meta_data_file": meta_data_file
                }
            }
        }
    )

    return plx.processing.create_input_data_fn(mode=plx.Modes.EVAL,
                                               pipeline_config=config.pipeline_config)


def experiment_fn(output_dir):
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
    dataset_dir = '../data/cifar10'
    plx.datasets.cifar10.prepare(dataset_dir)
    train_data_file = plx.datasets.cifar10.RECORD_FILE_NAME_FORMAT.format(dataset_dir,
                                                                          plx.Modes.TRAIN)
    eval_data_file = plx.datasets.cifar10.RECORD_FILE_NAME_FORMAT.format(dataset_dir,
                                                                         plx.Modes.EVAL)
    meta_data_file = plx.datasets.cifar10.MEAT_DATA_FILENAME_FORMAT.format(dataset_dir)

    run_config = plx.configs.RunConfig(save_checkpoints_steps=100)
    experiment = plx.experiments.Experiment(
        estimator=plx.estimators.Estimator(model_fn=model_fn, model_dir=output_dir,
                                           config=run_config),
        train_input_fn=get_train_input_fn(train_data_file, meta_data_file),
        eval_input_fn=get_eval_input_fn(eval_data_file, meta_data_file),
        train_steps=1000,
        eval_steps=10,
        eval_every_n_steps=5)

    return experiment


def main(*args):
    plx.experiments.run_experiment(experiment_fn=experiment_fn,
                                   output_dir="/tmp/polyaxon_logs/res_net_cifar10",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
