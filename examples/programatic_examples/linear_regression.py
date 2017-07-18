# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np
import tensorflow as tf
import polyaxon as plx

from tensorflow.python.estimator.inputs.numpy_io import numpy_input_fn

tf.logging.set_verbosity(tf.logging.INFO)

X = np.linspace(-1, 1, 100)
y = 2 * X + np.random.randn(*X.shape) * 0.33

# Test a data set
X_val = np.linspace(1, 1.5, 10)
y_val = 2 * X_val + np.random.randn(*X_val.shape) * 0.33


def graph_fn(mode, inputs):
    return plx.layers.SingleUnit(mode)(inputs['X'])


def model_fn(features, labels, mode):
    model = plx.models.Regressor(
        mode, graph_fn=graph_fn, loss_config=plx.configs.LossConfig(module='mean_squared_error'),
        optimizer_config=plx.configs.OptimizerConfig(module='sgd', learning_rate=0.009),
        eval_metrics_config=[],
        summaries='all', name='regressor')
    return model(features, labels)


estimator = plx.estimators.Estimator(model_fn=model_fn, model_dir="/tmp/polyaxon_logs/linear")

estimator.train(input_fn=numpy_input_fn(
    {'X': X}, y, shuffle=False, num_epochs=10000, batch_size=len(X)))

print([x['results'] for x in estimator.predict(input_fn=numpy_input_fn({'X': X_val}, shuffle=False))])
print(y_val)
