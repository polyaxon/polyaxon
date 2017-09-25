# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx

from polyaxon_schemas.losses import SigmoidCrossEntropyConfig
from polyaxon_schemas.metrics import AccuracyConfig
from polyaxon_schemas.optimizers import AdamConfig


def graph_fn(mode, features):
    x = plx.layers.Conv2D(filters=32, kernel_size=3, activation='relu')(features['image'])
    x = plx.layers.MaxPooling2D(pool_size=2)(x)
    x = plx.layers.Conv2D(filters=64, kernel_size=3, activation='relu')(x)
    x = plx.layers.Conv2D(filters=64, kernel_size=3, activation='relu')(x)
    x = plx.layers.MaxPooling2D(pool_size=2)(x)
    x = plx.layers.Flatten()(x)
    x = plx.layers.Dense(units=512, activation='tanh')(x)
    x = plx.layers.Dropout(rate=0.5)(x)
    x = plx.layers.Dense(units=10)(x)
    return x


def model_fn(features, labels, params, mode, config):
    model = plx.models.Classifier(
        mode=mode,
        graph_fn=graph_fn,
        loss_config=SigmoidCrossEntropyConfig(),
        optimizer_config=AdamConfig(learning_rate=0.001),
        eval_metrics_config=[AccuracyConfig()],
        summaries=['loss'],
        one_hot_encode=True,
        n_classes=10)
    return model(features=features, labels=labels, params=params, config=config)


def experiment_fn(output_dir):
    """Creates an experiment using cnn for CIFAR-10 dataset classification task.

    References:
        * Learning Multiple Layers of Features from Tiny Images, A. Krizhevsky, 2009.

    Links:
        * [CIFAR-10 Dataset](https://www.cs.toronto.edu/~kriz/cifar.html)
    """
    dataset_dir = '../data/cifar10'
    plx.datasets.cifar10.prepare(dataset_dir)
    train_input_fn, eval_input_fn = plx.datasets.cifar10.create_input_fn(dataset_dir)

    experiment = plx.experiments.Experiment(
        estimator=plx.estimators.Estimator(model_fn=model_fn, model_dir=output_dir),
        train_input_fn=train_input_fn,
        eval_input_fn=eval_input_fn,
        train_steps=1000,
        eval_steps=10,
        eval_every_n_steps=5)

    return experiment


def main(*args):
    plx.experiments.run_experiment(experiment_fn=experiment_fn,
                                   output_dir="/tmp/polyaxon_logs/convnet_cifar10",
                                   schedule='continuous_train_and_eval')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
