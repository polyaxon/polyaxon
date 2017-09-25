# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

import polyaxon as plx


def experiment_fn(output_dir):
    """Creates an experiment using Lenet network.

    Links:
        * http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf
    """
    plx.datasets.mnist.prepare('../data/mnist')

    config = './yaml_configs/lenet.yml'
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=experiment_fn,
                                   output_dir="/tmp/polyaxon_logs/lenet",
                                   schedule='continuous_train_and_eval')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
