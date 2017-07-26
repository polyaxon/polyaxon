# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx


def main(*args):
    """Creates an experiment using a highway network.

    Links:
        * [MNIST Dataset] http://yann.lecun.com/exdb/mnist/
        * [https://arxiv.org/abs/1505.00387](https://arxiv.org/abs/1505.00387)
    """
    def graph_fn(mode, features):
        x = plx.layers.FullyConnected(
            mode, num_units=64, activation='elu', regularizer='l2_regularizer')(features['image'])

        for i in range(10):
            x = plx.layers.Highway(mode, num_units=64, activation='elu',
                                   regularizer='l2_regularizer', transform_dropout=0.8)(x)

        return plx.layers.FullyConnected(mode, num_units=10)(x)

    def model_fn(features, labels, mode):
        model = plx.models.Classifier(
            mode, graph_fn=graph_fn, summaries='loss',
            eval_metrics_config=[plx.configs.MetricConfig(module='streaming_accuracy')],
            n_classes=10, one_hot_encode=True)
        return model(features, labels)

    estimator = plx.estimators.Estimator(model_fn=model_fn,
                                         model_dir="/tmp/polyaxon_logs/highway_dnn")

    train_input_fn, eval_input_fn = plx.datasets.mnist.create_input_fn('../data/mnist')
    xp = plx.experiments.Experiment(estimator=estimator, train_input_fn=train_input_fn,
                                    eval_input_fn=eval_input_fn, eval_every_n_steps=10)
    xp.continuous_train_and_evaluate()


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()

