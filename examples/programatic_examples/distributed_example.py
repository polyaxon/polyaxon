# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import numpy as np
import tensorflow as tf
import polyaxon as plx

tf.logging.set_verbosity(tf.logging.INFO)


def create_experiment(task_type, task_index=0):
    def graph_fn(mode, features):
        x = plx.layers.FullyConnected(mode, num_units=32, activation='tanh')(features['X'])
        return plx.layers.FullyConnected(mode, num_units=1, activation='sigmoid')(x)

    def model_fn(features, labels, mode):
        model = plx.models.Regressor(
            mode, graph_fn=graph_fn,
            loss_config=plx.configs.LossConfig(module='absolute_difference'),
            optimizer_config=plx.configs.OptimizerConfig(module='sgd', learning_rate=0.5,
                                                         decay_type='exponential_decay',
                                                         decay_steps=10),
            summaries='all', name='xor')
        return model(features, labels)

    os.environ['task_type'] = task_type
    os.environ['task_index'] = str(task_index)

    cluster_config = {
        'master': ['127.0.0.1:9000'],
        'ps': ['127.0.0.1:9001'],
        'worker': ['127.0.0.1:9002'],
        'environment': 'cloud'
    }

    config = plx.configs.RunConfig(cluster_config=cluster_config)

    est = plx.estimators.Estimator(model_fn=model_fn, model_dir="/tmp/polyaxon_logs/xor",
                                   config=config)

    # Data
    x = np.asarray([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
    y = np.asarray([[0], [1], [1], [0]])

    def input_fn(num_epochs=1):
        return plx.processing.numpy_input_fn({'X': x}, y,
                                             shuffle=False,
                                             num_epochs=num_epochs,
                                             batch_size=len(x))

    return plx.experiments.Experiment(est, input_fn(10000), input_fn(100))
