# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx


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
    plx.datasets.flowers17.prepare('../data/flowers17')

    config = './yaml_configs/alexnet_flower17.yml'
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=experiment_fn,
                                   output_dir="/tmp/polyaxon_logs/alexnet_flowers17",
                                   schedule='continuous_train_and_eval')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
