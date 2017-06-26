# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np
import tensorflow as tf
from tensorflow.python.framework import constant_op
import polyaxon as plx

from tensorflow.python.estimator.inputs.numpy_io import numpy_input_fn

tf.logging.set_verbosity(tf.logging.INFO)


# Data
X = np.asarray([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
y = np.asarray([[0], [1], [1], [0]])


def graph_fn(mode, inputs):
    x = plx.layers.FullyConnected(mode, num_units=32, activation='tanh')(inputs['X'])
    return plx.layers.FullyConnected(mode, num_units=1, activation='sigmoid')(x)


def model_fn(features, labels, mode):
    model = plx.models.Regressor(
        mode, graph_fn=graph_fn, loss_config=plx.configs.LossConfig(module='absolute_difference'),
        optimizer_config=plx.configs.OptimizerConfig(module='adam', learning_rate=0.5),
        summaries='all', name='xor')
    return model(features, labels)


estimator = plx.experiments.Estimator(model_fn=model_fn, model_dir="/tmp/polyaxon_logs/xor")


def input_fn(num_epochs=1):
    return numpy_input_fn({'X': X}, y,
                          shuffle=False,
                          num_epochs=num_epochs,
                          batch_size=len(X))

# estimator.train(input_fn(1))

def input_fn():
    return {'X': constant_op.constant(X)}, constant_op.constant(y)

print([x['results'] for x in estimator.predict(input_fn)])
print(y)
