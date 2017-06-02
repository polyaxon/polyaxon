from __future__ import absolute_import, division, print_function

from sklearn import datasets
from sklearn import model_selection
from sklearn import preprocessing
from tensorflow.python.estimator.inputs.numpy_io import numpy_input_fn

import numpy as np
import polyaxon as plx
import tensorflow as tf


def main(*args):
    # Load dataset
    boston = datasets.load_boston()
    x, y = boston.data, boston.target

    # Split dataset into train / test
    x_train, x_test, y_train, y_test = model_selection.train_test_split(
        x, y, test_size=0.2, random_state=42)

    # Scale data (training set) to 0 mean and unit standard deviation.
    scaler = preprocessing.StandardScaler()
    x_train = scaler.fit_transform(x_train)

    def graph_fn(mode, inputs):
        x = plx.layers.FullyConnected(
            mode, num_units=32, activation='relu', dropout=0.3)(inputs['x'])
        x = plx.layers.FullyConnected(mode, num_units=32, activation='relu', dropout=0.3)(x)
        return plx.layers.FullyConnected(mode, num_units=1, dropout=0.3)(x)

    def model_fn(features, labels, mode):
        model = plx.experiments.RegressorModel(
            mode, graph_fn=graph_fn, loss_config=plx.configs.LossConfig(name='mean_squared_error'),
            optimizer_config=plx.configs.OptimizerConfig(name='SGD', learning_rate=0.01),
            summaries='all', name='regressor')
        return model(features, labels)

    estimator = plx.experiments.Estimator(model_fn=model_fn,
                                          model_dir="/tmp/polyaxon_logs/boston")

    # Fit
    estimator.train(input_fn=numpy_input_fn(
        {'x': np.asarray(x_train, dtype=np.float32)}, np.expand_dims(y_train, axis=1),
        shuffle=False, num_epochs=5000, batch_size=64))

    # Transform
    x_test = scaler.transform(x_test)

    # Predict and score
    estimator.evaluate(input_fn=numpy_input_fn(
        {'x': np.asarray(x_test, dtype=np.float32)}, np.expand_dims(y_test, axis=1),
        shuffle=False, num_epochs=1, batch_size=32))


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
