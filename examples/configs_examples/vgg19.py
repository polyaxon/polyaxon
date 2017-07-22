# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx


def experiment_fn(output_dir):
    """Creates an experiement using a VGG19 to mnist Dataset.

    References:
        * Very Deep Convolutional Networks for Large-Scale Image Recognition.
        K. Simonyan, A. Zisserman. arXiv technical report, 2014.

    Links:
        * http://arxiv.org/pdf/1409.1556
    """
    plx.datasets.mnist.prepare('../data/mnist')

    config = './yaml_configs/vgg19.yml'
    # or
    config = './json_configs/vgg19.json'
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=experiment_fn,
                                   output_dir="/tmp/polyaxon_logs/vgg19",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
