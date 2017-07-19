# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx


def create_experiment_json_fn(output_dir):
    """Creates an experiment using cnn for MNIST dataset classification task."""
    config = './yaml_configs/conv_highway_mnist.yml'
    # or
    config = './json_configs/conv_highway_mnist.json'
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=create_experiment_json_fn,
                                   output_dir="/tmp/polyaxon_logs/conv_highway_mnsit",
                                   schedule="continuous_train_and_evaluate")


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
