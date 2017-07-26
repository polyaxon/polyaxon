# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np
import polyaxon as plx
import tensorflow as tf

from sklearn import datasets
from sklearn import model_selection
from sklearn import preprocessing

from tensorflow.python.estimator.inputs.numpy_io import numpy_input_fn


def main(*args):
    """Creates an estimator for the boston house-prices datase.

    References:
        * This dataset concerns housing values in Boston suburbs.
        It's based on the "Boston Housing Dataset" from University of California, Irvine,
        which in turn was taken from the StatLib library maintained at Carnegie Mellon University.

    Returns:
        * https://archive.ics.uci.edu/ml/datasets/Housing
    """
    # Load dataset
    boston = datasets.load_boston()
    x, y = boston.data, boston.target

    # Split dataset into train / test
    x_train, x_test, y_train, y_test = model_selection.train_test_split(
        x, y, test_size=0.2, random_state=42)

    # Scale data (training set) to 0 mean and unit standard deviation.
    scaler = preprocessing.StandardScaler()
    x_train = scaler.fit_transform(x_train)

    def graph_fn(mode, features):
        x = plx.layers.FullyConnected(
            mode, num_units=32, activation='relu', dropout=0.3)(features['x'])
        x = plx.layers.FullyConnected(mode, num_units=32, activation='relu', dropout=0.3)(x)
        return plx.layers.FullyConnected(mode, num_units=1, dropout=0.3)(x)

    def model_fn(features, labels, mode):
        model = plx.models.Regressor(
            mode, graph_fn=graph_fn,
            loss_config=plx.configs.LossConfig(module='mean_squared_error'),
            optimizer_config=plx.configs.OptimizerConfig(module='sgd', learning_rate=0.01),
            summaries='all')
        return model(features, labels)

    estimator = plx.estimators.Estimator(model_fn=model_fn,
                                         model_dir="/tmp/polyaxon_logs/boston")

    estimator.train(input_fn=numpy_input_fn(
        {'x': np.asarray(x_train, dtype=np.float32)}, np.expand_dims(y_train, axis=1),
        shuffle=False, num_epochs=5000, batch_size=64))

    x_test = scaler.transform(x_test)

    estimator.evaluate(input_fn=numpy_input_fn(
        {'x': np.asarray(x_test, dtype=np.float32)}, np.expand_dims(y_test, axis=1),
        shuffle=False, num_epochs=1, batch_size=32))


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
