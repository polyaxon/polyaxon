# Polyaxon

Deep Learning library for TensorFlow for building end to end models and experiments.

# Design Goals

Polyaxon was built with the following goals:

 * Modularity: The creation of a computation graph based on modular and understandable modules,
    with the possibility to reuse and share the module in subsequent usage.

 * Usability: Training a model should be easy enough, and should enable quick experimentations.

 * Configurable: Models and experiments could be created using a YAML/Json file, but also in python files.

 * Extensibility: The modularity and the extensive documentation of the code makes it easy to build and extend the set of provided modules.

 * Performance: Polyaxon is based on internal `tensorflow` code base and leverage the builtin distributed learning.

 * Data Preprocessing: Polyaxon provides many pipelines and data processor to support different data inputs.


# Quick start

## A classification problem

```python
    X_train, Y_train, X_test, Y_test = load_mnist()

    config = {
        'name': 'lenet_mnsit',
        'output_dir': output_dir,
        'eval_every_n_steps': 1,
        'train_steps_per_iteration': 100,
        'run_config': {'save_checkpoints_steps': 100},
        'train_input_data_config': {
            'input_type': plx.configs.InputDataConfig.NUMPY,
            'pipeline_config': {'name': 'train',
                                'batch_size': 64,
                                'num_epochs': None,
                                'shuffle': True},
            'x': X_train,
            'y': Y_train
        },
        'eval_input_data_config': {
            'input_type': plx.configs.InputDataConfig.NUMPY,
            'pipeline_config': {'name': 'eval',
                                'batch_size': 32,
                                'num_epochs': None,
                                'shuffle': False},
            'x': X_test,
            'y': Y_test
        },
        'estimator_config': {'output_dir': output_dir},
        'model_config': {
            'model_type': 'classifier',
            'loss_config': {'name': 'softmax_cross_entropy'},
            'eval_metrics_config': [{'name': 'streaming_accuracy'},
                                    {'name': 'streaming_precision'}],
            'optimizer_config': {'name': 'Adam', 'learning_rate': 0.002, 
                                 'decay_type': 'exponential_decay', 
                                 'decay_rate': 0.2},
            'graph_config': {
                'name': 'lenet',
                'definition': [
                    (plx.layers.Conv2d, {'num_filter': 32, 
                                         'filter_size': 5, 
                                         'strides': 1, 
                                         'regularizer': 'l2_regularizer'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2}),
                    (plx.layers.Conv2d, {'num_filter': 64, 
                                         'filter_size': 5, 
                                         'regularizer': 'l2_regularizer'}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2}),
                    (plx.layers.FullyConnected, {'n_units': 1024, 'activation': 'tanh'}),
                    (plx.layers.FullyConnected, {'n_units': 10}),
                ]
            }
        }
    }
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    xp = plx.experiments.create_experiment(experiment_config)
    xp.continuous_train_and_evaluate()
```

## A regression problem

```python
    X, y = generate_data(np.sin, np.linspace(0, 100, 10000, dtype=np.float32), time_steps=7)

    config = {
        'name': 'time_series',
        'output_dir': output_dir,
        'eval_every_n_steps': 5,
        'run_config': {'save_checkpoints_steps': 100},
        'train_input_data_config': {
            'input_type': plx.configs.InputDataConfig.NUMPY,
            'pipeline_config': {'name': 'train',
                                'batch_size': 64,
                                'num_epochs': None,
                                'shuffle': False},
            'x': X['train'],
            'y': y['train']
        },
        'eval_input_data_config': {
            'input_type': plx.configs.InputDataConfig.NUMPY,
            'pipeline_config': {'name': 'eval',
                                'batch_size': 32,
                                'num_epochs': None,
                                'shuffle': False},
            'x': X['val'],
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
                'definition': [
                    (plx.layers.LSTM, {'num_units': 7, 'num_layers': 1}),
                    # (Slice, {'begin': [0, 6], 'size': [-1, 1]}),
                    (plx.layers.FullyConnected, {'n_units': 1}),
                ]
            }
        }
    }
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    xp = plx.experiments.create_experiment(experiment_config)
    xp.continuous_train_and_evaluate()
```

# Installation

To install the latest version of Polyaxon: `pip install polyaxon`

Alternatively, you can also install from source by running (from source folder): `python setup.py install`

# Examples

Some example are provided [here](examples), more examples and use case will pushed, a contribution with an example is also appreciated.

# Contributions

Please follow the contribution guide line: *[Contribute to Polyaxon](CONTRIBUTING.md)*.

# License

MIT License

# Credit

This work is based and was inspired from different projects, `tensorflow.contrib.learn`, `keras`, `sonnet`, and `seq2seq`.
The idea behind creating this library is to provide a tool that allow engineers and researchers to develop and experiment with end to end solution.
This would allow us to have a complete control over the api and future design decision.
