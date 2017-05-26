# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np
import tensorflow as tf
import polyaxon as plx

from tensorflow.python.estimator.inputs.numpy_io import numpy_input_fn

tf.logging.set_verbosity(tf.logging.INFO)


# Data
X = np.asarray([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
y = np.asarray([[0], [1], [1], [0]])


def graph_fn(mode, inputs):
    x = plx.layers.FullyConnected(mode, n_units=8, activation='tanh')(inputs)
    return plx.layers.FullyConnected(mode, n_units=1, activation='sigmoid')(x)


def model_fn(features, labels, mode):
    model = plx.experiments.RegressorModel(
        mode, graph_fn=graph_fn, loss_config=plx.configs.LossConfig(name='absolute_difference'),
        optimizer_config=plx.configs.OptimizerConfig(name='SGD', learning_rate=0.9),
        summaries='all', name='xor')
    return model(features, labels)


estimator = plx.experiments.Estimator(model_fn=model_fn, model_dir="/tmp/polyaxon_logs/xor")


def input_fn(num_epochs=1):
    return numpy_input_fn({'X': X}, y,
                          shuffle=False,
                          num_epochs=num_epochs,
                          batch_size=len(X))

estimator.train(input_fn(10000))

print([x['results'] for x in estimator.predict(input_fn())])
print(y)
