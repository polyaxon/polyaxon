# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

import numpy as np
import tensorflow as tf
from polyaxon_schemas.settings import RunConfig, ClusterConfig

import polyaxon as plx

from polyaxon_schemas.losses import AbsoluteDifferenceConfig
from polyaxon_schemas.optimizers import SGDConfig

tf.logging.set_verbosity(tf.logging.INFO)


def create_experiment(task_type, task_id=0):
    def graph_fn(mode, features):
        x = plx.layers.Dense(units=32, activation='tanh')(features['X'])
        return plx.layers.Dense(units=1, activation='sigmoid')(x)

    def model_fn(features, labels, mode):
        model = plx.models.Regressor(
            mode, graph_fn=graph_fn,
            loss=AbsoluteDifferenceConfig(),
            optimizer=SGDConfig(learning_rate=0.5,
                                decay_type='exponential_decay',
                                decay_steps=10),
            summaries='all', name='xor')
        return model(features, labels)

    config = RunConfig(cluster=ClusterConfig(master=['127.0.0.1:9000'],
                                             worker=['127.0.0.1:9002'],
                                             ps=['127.0.0.1:9001']))

    config = plx.estimators.RunConfig.from_config(config)
    config = config.replace(task_type=task_type, task_id=task_id)

    est = plx.estimators.Estimator(model_fn=model_fn, model_dir="/tmp/polyaxon_logs/xor",
                                   config=config)

    # Data
    x = np.asarray([[0., 0.], [0., 1.], [1., 0.], [1., 1.]], dtype=np.float32)
    y = np.asarray([[0], [1], [1], [0]], dtype=np.float32)

    def input_fn(num_epochs=1):
        return plx.processing.numpy_input_fn({'X': x}, y,
                                             shuffle=False,
                                             num_epochs=num_epochs,
                                             batch_size=len(x))

    return plx.experiments.Experiment(est, input_fn(10000), input_fn(100))


# >> create_experiment('master').train_and_evaluate()
# >> create_experiment('worker').train()
# >> create_experiment('ps').run_std_server()
