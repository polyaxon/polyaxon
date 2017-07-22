# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx


def experiment_fn(output_dir):
    """Creates an experiment using cnn for CIFAR-10 dataset classification task.

    References:
        * Learning Multiple Layers of Features from Tiny Images, A. Krizhevsky, 2009.

    Links:
        * [CIFAR-10 Dataset](https://www.cs.toronto.edu/~kriz/cifar.html)
    """
    plx.datasets.cifar10.prepare('../data/conv_cifar10')

    config = './yaml_configs/conv_cifar10.yml'
    # or
    config = './json_configs/conv_cifar10.json'
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=experiment_fn,
                                   output_dir="/tmp/polyaxon_logs/convnet_cifar10",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
