# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from six.moves import xrange

import numpy as np

try:
    import pandas as pd
except ImportError:
    pass

import polyaxon as plx


def x_sin(x):
    return x * np.sin(x)


def sin_cos(x):
    return pd.DataFrame(dict(a=np.sin(x), b=np.cos(x)), index=x)


def rnn_data(data, time_steps, labels=False):
    """
    creates new data frame based on previous observation
      * example:
        l = [1, 2, 3, 4, 5]
        time_steps = 2
        -> labels == False [[1, 2], [2, 3], [3, 4]]
        -> labels == True [3, 4, 5]
    """
    rnn_df = []
    for i in xrange(len(data) - time_steps):
        if labels:
            try:
                rnn_df.append(data.iloc[i + time_steps].as_matrix())
            except AttributeError:
                rnn_df.append(data.iloc[i + time_steps])
        else:
            data_ = data.iloc[i: i + time_steps].as_matrix()
            rnn_df.append(data_ if len(data_.shape) > 1 else [[i] for i in data_])

    return np.array(rnn_df, dtype=np.float32)


def split_data(data, val_size=0.1, test_size=0.1):
    """
    splits data to training, validation and testing parts
    """
    ntest = int(round(len(data) * (1 - test_size)))
    nval = int(round(len(data.iloc[:ntest]) * (1 - val_size)))

    df_train, df_val, df_test = data.iloc[:nval], data.iloc[nval:ntest], data.iloc[ntest:]

    return df_train, df_val, df_test


def prepare_data(data, time_steps, labels=False, val_size=0.1, test_size=0.1):
    """
    Given the number of `time_steps` and some data,
    prepares training, validation and test data for an lstm cell.
    """
    df_train, df_val, df_test = split_data(data, val_size, test_size)
    return (rnn_data(df_train, time_steps, labels=labels),
            rnn_data(df_val, time_steps, labels=labels),
            rnn_data(df_test, time_steps, labels=labels))


def generate_data(fct, x, time_steps, seperate=False):
    """generates data with based on a function fct"""
    data = fct(x)
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    train_x, val_x, test_x = prepare_data(data['a'] if seperate else data, time_steps)
    train_y, val_y, test_y = prepare_data(data['b'] if seperate else data, time_steps, labels=True)
    return dict(train=train_x, val=val_x, test=test_x), dict(train=train_y, val=val_y, test=test_y)


def experiment_fn(output_dir, X, y, train_steps=1000, num_units=7, output_units=1, num_layers=1):
    """Creates an experiment using LSTM architecture for timeseries regression problem."""

    def graph_fn(mode, features):
        x = plx.layers.LSTM(mode=mode, num_units=num_units, num_layers=num_layers)(features['x'])
        return plx.layers.FullyConnected(mode=mode, num_units=output_units)(x)

    def model_fn(features, labels, mode):
        return plx.models.Regressor(
            mode=mode,
            graph_fn=graph_fn,
            loss_config=plx.configs.LossConfig(module='mean_squared_error'),
            optimizer_config=plx.configs.OptimizerConfig(module='adagrad', learning_rate=0.1),
            eval_metrics_config=[
                plx.configs.MetricConfig(module='streaming_root_mean_squared_error'),
                plx.configs.MetricConfig(module='streaming_mean_absolute_error')
            ]
        )(features=features, labels=labels)

    run_config = plx.configs.RunConfig(save_checkpoints_steps=100)
    return plx.experiments.Experiment(
        estimator=plx.estimators.Estimator(
            model_fn=model_fn, model_dir=output_dir, config=run_config),
        train_input_fn=plx.processing.numpy_input_fn(
            x={'x': X['train']}, y=y['train'], batch_size=64, num_epochs=None, shuffle=False),
        eval_input_fn=plx.processing.numpy_input_fn(
            x={'x': X['train']}, y=y['train'], batch_size=32, num_epochs=None, shuffle=False),
        train_steps=train_steps,
        eval_steps=10,
        eval_every_n_steps=5)
