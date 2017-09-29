# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx

from polyaxonfile.manager import prepare_experiments


def experiment_fn(output_dir):
    """Creates an experiment using cnn for CIFAR-10 dataset classification task.

    References:
        * Learning Multiple Layers of Features from Tiny Images, A. Krizhevsky, 2009.

    Links:
        * [CIFAR-10 Dataset](https://www.cs.toronto.edu/~kriz/cifar.html)
    """
    plx.datasets.cifar10.prepare('../data/cifar10')

    config = './yaml_configs/convnet_cifar10.yml'
    return prepare_experiments(config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=experiment_fn,
                                   output_dir="/tmp/polyaxon_logs/convnet_cifar10",
                                   schedule='continuous_train_and_eval')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
