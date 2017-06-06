# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from six.moves import xrange

import numpy as np
try:
    import pandas as pd
except ImportError:
    pass
import tensorflow as tf
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


def create_experiment_json_fn(output_dir):
    """Creates an experiment using LSTM architecture for timeseries regression problem."""
    X, y = generate_data(sin_cos, np.linspace(0, 100, 10000, dtype=np.float32), 7, seperate=False)

    config = {
        'name': 'time_series',
        'output_dir': output_dir,
        'eval_every_n_steps': 5,
        'train_steps_per_iteration': 100,
        'run_config': {'save_checkpoints_steps': 100},
        'train_input_data_config': {
            'input_type': plx.configs.InputDataConfig.NUMPY,
            'pipeline_config': {'name': 'train', 'batch_size': 64, 'num_epochs': None,
                                'shuffle': False},
            'x': {'x': X['train']},
            'y': y['train']
        },
        'eval_input_data_config': {
            'input_type': plx.configs.InputDataConfig.NUMPY,
            'pipeline_config': {'name': 'eval', 'batch_size': 32, 'num_epochs': None,
                                'shuffle': False},
            'x': {'x': X['val']},
            'y': y['val']
        },
        'estimator_config': {'output_dir': output_dir},
        'model_config': {
            'model_type': 'regressor',
            'loss_config': {'name': 'mean_squared_error'},
            'eval_metrics_config': [{'name': 'streaming_root_mean_squared_error'},
                                    {'name': 'streaming_mean_absolute_error'}],
            'optimizer_config': {'name': 'Adagrad', 'learning_rate': 0.1},
            'graph_config': {
                'name': 'regressor',
                'features': ['x'],
                'definition': [
                    (plx.layers.LSTM, {'num_units': 7, 'num_layers': 1}),
                    # (Slice, {'begin': [0, 6], 'size': [-1, 1]}),
                    (plx.layers.FullyConnected, {'num_units': 2}),
                ]
            }
        }
    }
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=create_experiment_json_fn,
                                   output_dir="/tmp/polyaxon_logs/timeseries",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
