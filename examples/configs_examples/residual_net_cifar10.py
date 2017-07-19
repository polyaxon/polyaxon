# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx


def create_experiment_json_fn(output_dir):
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
    config = './yaml_configs/residual_net_cifar10.yml'
    # or
    config = './json_configs/residual_net_cifar10.json'
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=create_experiment_json_fn,
                                   output_dir="/tmp/polyaxon_logs/res_net_cifar10",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
