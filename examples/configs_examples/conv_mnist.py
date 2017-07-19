# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx


def create_experiment_json_fn(output_dir):
    """Creates an experiment using cnn for MNIST dataset classification task.

    References:
        * Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner. "Gradient-based learning applied to
        document recognition." Proceedings of the IEEE, 86(11):2278-2324, November 1998.
    Links:
        * [MNIST Dataset] http://yann.lecun.com/exdb/mnist/
    """
    config = './yaml_configs/conv_mnist.yml'
    # or
    config = './json_configs/conv_mnist.json'
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=create_experiment_json_fn,
                                   output_dir="/tmp/polyaxon_logs/conv_mnsit",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
