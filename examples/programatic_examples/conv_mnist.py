# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

import polyaxon as plx


def graph_fn(mode, inputs):
    x = plx.layers.Conv2d(mode=mode, num_filter=32, filter_size=3, strides=1, activation='elu',
                          regularizer='l2_regularizer')(inputs['image'])
    x = plx.layers.MaxPool2d(mode=mode, kernel_size=2)(x)
    x = plx.layers.LocalResponseNormalization(mode=mode)(x)
    x = plx.layers.Conv2d(mode=mode, num_filter=64, filter_size=3, activation='relu',
                          regularizer='l2_regularizer')(x)
    x = plx.layers.MaxPool2d(mode=mode, kernel_size=2)(x)
    x = plx.layers.LocalResponseNormalization(mode=mode)(x)
    x = plx.layers.FullyConnected(mode=mode, num_units=128, activation='tanh')(x)
    x = plx.layers.Dropout(mode=mode, keep_prob=0.8)(x)
    x = plx.layers.FullyConnected(mode=mode, num_units=256, activation='tanh')(x)
    x = plx.layers.Dropout(mode=mode, keep_prob=0.8)(x)
    x = plx.layers.FullyConnected(mode=mode, num_units=10)(x)
    return x


def model_fn(features, labels, params, mode, config):
    model = plx.models.Classifier(
        mode=mode,
        graph_fn=graph_fn,
        loss_config=plx.configs.LossConfig(module='sigmoid_cross_entropy'),
        optimizer_config=plx.configs.OptimizerConfig(module='adam', learning_rate=0.001),
        eval_metrics_config=[plx.configs.MetricConfig(module='streaming_accuracy')],
        summaries='all',
        one_hot_encode=True,
        n_classes=10)
    return model(features=features, labels=labels, params=params, config=config)


def experiment_fn(output_dir):
    """Creates an experiment using cnn for MNIST dataset classification task.

    References:
        * Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner. "Gradient-based learning applied to
        document recognition." Proceedings of the IEEE, 86(11):2278-2324, November 1998.
    Links:
        * [MNIST Dataset] http://yann.lecun.com/exdb/mnist/
    """
    dataset_dir = './data/mnist'
    plx.datasets.mnist.prepare(dataset_dir)
    train_input_fn, eval_input_fn = plx.datasets.mnist.create_input_fn(dataset_dir)

    run_config = plx.configs.RunConfig(save_checkpoints_steps=100)
    experiment = plx.experiments.Experiment(
        estimator=plx.estimators.Estimator(model_fn=model_fn, model_dir=output_dir,
                                           config=run_config),
        train_input_fn=train_input_fn,
        eval_input_fn=eval_input_fn,
        train_steps=1000,
        eval_steps=10,
        eval_every_n_steps=5)

    return experiment


def main(*args):
    plx.experiments.run_experiment(experiment_fn=experiment_fn,
                                   output_dir="/tmp/polyaxon_logs/conv_mnsit",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
