# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import polyaxon as plx


def create_experiment(output_dir, X, y, train_steps=1000, num_units=7, output_units=1, num_layers=1):
    """Creates an experiment using LSTM architecture for timeseries regression problem."""

    config = {
        'name': 'time_series',
        'output_dir': output_dir,
        'eval_every_n_steps': 100,
        'train_steps_per_iteration': 100,
        'train_steps': train_steps,
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
            'module': 'Regressor',
            'loss_config': {'module': 'mean_squared_error'},
            'eval_metrics_config': [{'module': 'streaming_root_mean_squared_error'},
                                    {'module': 'streaming_mean_absolute_error'}],
            'optimizer_config': {'module': 'adagrad', 'learning_rate': 0.1},
            'graph_config': {
                'name': 'regressor',
                'features': ['x'],
                'definition': [
                    (plx.layers.LSTM, {'num_units': num_units, 'num_layers': num_layers}),
                    (plx.layers.FullyConnected, {'num_units': output_units}),
                ]
            }
        }
    }
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)
