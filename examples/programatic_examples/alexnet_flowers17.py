# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx

from polyaxon_schemas.optimizers import MomentumConfig
from polyaxon_schemas.losses import SigmoidCrossEntropyConfig
from polyaxon_schemas.metrics import AccuracyConfig

from polyaxon.regularizations import l2


def graph_fn(mode, features):
    x = plx.layers.Conv2D(filters=96, kernel_size=11, strides=4, activation='relu',
                          kernel_regularizer=l2(0.02))(features['image'])
    x = plx.layers.MaxPooling2D(pool_size=3, strides=2)(x)
    x = plx.layers.Conv2D(filters=156, kernel_size=5, activation='relu',
                          kernel_regularizer=l2(0.02))(x)
    x = plx.layers.MaxPooling2D(pool_size=3, strides=2)(x)
    x = plx.layers.Conv2D(filters=384, kernel_size=3, activation='relu')(x)
    x = plx.layers.Conv2D(filters=384, kernel_size=3, activation='relu')(x)
    x = plx.layers.Conv2D(filters=256, kernel_size=3, activation='relu')(x)
    x = plx.layers.MaxPooling2D(pool_size=3, strides=2)(x)
    x = plx.layers.Flatten()(x)
    x = plx.layers.Dense(units=4096, activation='tanh')(x)
    x = plx.layers.Dropout(rate=0.5)(x)
    x = plx.layers.Dense(units=4096, activation='tanh')(x)
    x = plx.layers.Dropout(rate=0.5)(x)
    x = plx.layers.Dense(units=17)(x)
    return x


def model_fn(features, labels, params, mode, config):
    model = plx.models.Classifier(
        mode=mode,
        graph_fn=graph_fn,
        loss_config=SigmoidCrossEntropyConfig(),
        optimizer_config=MomentumConfig(learning_rate=0.001),
        eval_metrics_config=[AccuracyConfig()],
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
        * [AlexNet Paper](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)  # noqa
        * [Flower Dataset (17)](http://www.robots.ox.ac.uk/~vgg/data/flowers/17/)
    """
    dataset_dir = '../data/flowers17'
    plx.datasets.flowers17.prepare(dataset_dir)
    train_input_fn, eval_input_fn = plx.datasets.flowers17.create_input_fn(dataset_dir)

    run_config = plx.estimators.RunConfig().replace(save_checkpoints_steps=100)
    experiment = plx.experiments.Experiment(
        estimator=plx.estimators.Estimator(model_fn=model_fn,
                                           model_dir=output_dir,
                                           config=run_config),
        train_input_fn=train_input_fn,
        eval_input_fn=eval_input_fn,
        train_steps=1000,
        eval_steps=10)

    return experiment


def main(*args):
    plx.experiments.run_experiment(experiment_fn=experiment_fn,
                                   output_dir="/tmp/polyaxon_logs/alexnet_flowers17",
                                   schedule='continuous_train_and_eval')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
