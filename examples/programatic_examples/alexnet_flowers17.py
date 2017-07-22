# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx


def graph_fn(mode, inputs):
    x = plx.layers.Conv2d(mode=mode, num_filter=96, filter_size=11, strides=4, activation='relu',
                          regularizer='l2_regularizer')(inputs['image'])
    x = plx.layers.MaxPool2d(mode=mode, kernel_size=3, strides=2)(x)
    x = plx.layers.LocalResponseNormalization(mode=mode)(x)
    x = plx.layers.Conv2d(mode=mode, num_filter=156, filter_size=5, activation='relu',
                          regularizer='l2_regularizer')(x)
    x = plx.layers.MaxPool2d(mode=mode, kernel_size=3, strides=2)(x)
    x = plx.layers.LocalResponseNormalization(mode=mode)(x)
    x = plx.layers.Conv2d(mode=mode, num_filter=384, filter_size=3, activation='relu')(x)
    x = plx.layers.Conv2d(mode=mode, num_filter=384, filter_size=3, activation='relu')(x)
    x = plx.layers.Conv2d(mode=mode, num_filter=256, filter_size=3, activation='relu')(x)
    x = plx.layers.MaxPool2d(mode=mode, kernel_size=3, strides=2)(x)
    x = plx.layers.LocalResponseNormalization(mode=mode)(x)
    x = plx.layers.FullyConnected(mode=mode, num_units=4096, activation='tanh', dropout=0.5)(x)
    x = plx.layers.FullyConnected(mode=mode, num_units=4096, activation='tanh', dropout=0.5)(x)
    x = plx.layers.FullyConnected(mode=mode, num_units=17)(x)
    return x


def model_fn(features, labels, params, mode, config):
    model = plx.models.Classifier(
        mode=mode,
        graph_fn=graph_fn,
        loss_config=plx.configs.LossConfig(module='sigmoid_cross_entropy'),
        optimizer_config=plx.configs.OptimizerConfig(module='momentum', learning_rate=0.001),
        eval_metrics_config=[plx.configs.MetricConfig(module='streaming_accuracy')],
        summaries=['loss'],
        one_hot_encode=True,
        n_classes=17)
    return model(features=features, labels=labels, params=params, config=config)


def experiment_fn(output_dir):
    """Creates an experiment using Alexnet applied to Oxford's 17  Category Flower Dataset.

    References:
        * Alex Krizhevsky, Ilya Sutskever & Geoffrey E. Hinton. ImageNet Classification with
        Deep Convolutional Neural Networks. NIPS, 2012.
        * 17 Category Flower Dataset. Maria-Elena Nilsback and Andrew Zisserman.

    Links:
        * [AlexNet Paper](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)
        * [Flower Dataset (17)](http://www.robots.ox.ac.uk/~vgg/data/flowers/17/)
    """
    dataset_dir = '../data/flowers17'
    plx.datasets.flowers17.prepare(dataset_dir)
    train_input_fn, eval_input_fn = plx.datasets.flowers17.create_input_fn(dataset_dir)

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
                                   output_dir="/tmp/polyaxon_logs/alexnet_flowers17",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
