[![Build Status](https://travis-ci.org/polyaxon/polyaxon.svg?branch=master)](https://travis-ci.org/polyaxon/polyaxon)
[![PyPI version](https://badge.fury.io/py/polyaxon.svg)](https://badge.fury.io/py/polyaxon)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/polyaxon/polyaxon)

# Polyaxon

Deep Learning and Reinforcement learning library for TensorFlow for building end to end models and experiments.

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

## A simple linear regression

```python
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
```


## A reinforcement learning problem

```python
env = plx.envs.GymEnvironment('CartPole-v0')

def graph_fn(mode, inputs):
    return plx.layers.FullyConnected(mode, num_units=512)(inputs['state'])

def model_fn(features, labels, mode):
    model = plx.models.DQNModel(
        mode, 
        graph_fn=graph_fn, 
        loss_config=plx.configs.LossConfig(module='huber_loss'),
        num_states=env.num_states, 
        num_actions=env.num_actions,
        optimizer_config=plx.configs.OptimizerConfig(module='sgd', learning_rate=0.01),
        exploration_config=plx.configs.ExplorationConfig(module='decay'),
        target_update_frequency=10, 
        dueling='mean', 
        summaries='all')
    return model(features, labels)

memory = plx.rl.memories.Memory(
    num_states=env.num_states, num_actions=env.num_actions, continuous=env.is_continuous)
agent = plx.estimators.Agent(
    model_fn=model_fn, memory=memory, model_dir="/tmp/polyaxon_logs/dqn_cartpole")

agent.train(env)
```


## A classification problem

```python
X_train, Y_train, X_test, Y_test = load_mnist()

config = {
    'name': 'lenet_mnsit',
    'output_dir': output_dir,
    'eval_every_n_steps': 10,
    'train_steps_per_iteration': 100,
    'run_config': {'save_checkpoints_steps': 100},
    'train_input_data_config': {
        'input_type': plx.configs.InputDataConfig.NUMPY,
        'pipeline_config': {'name': 'train', 'batch_size': 64, 'num_epochs': None,
                            'shuffle': True},
        'x': X_train,
        'y': Y_train
    },
    'eval_input_data_config': {
        'input_type': plx.configs.InputDataConfig.NUMPY,
        'pipeline_config': {'name': 'eval', 'batch_size': 32, 'num_epochs': None,
                            'shuffle': False},
        'x': X_test,
        'y': Y_test
    },
    'estimator_config': {'output_dir': output_dir},
    'model_config': {
        'summaries': 'all',
        'model_type': 'classifier',
        'loss_config': {'name': 'softmax_cross_entropy'},
        'eval_metrics_config': [{'name': 'streaming_accuracy'},
                                {'name': 'streaming_precision'}],
        'optimizer_config': {'name': 'Adam', 'learning_rate': 0.002,
                             'decay_type': 'exponential_decay', 'decay_rate': 0.2},
        'graph_config': {
            'name': 'lenet',
            'definition': [
                (plx.layers.Conv2d, {'num_filter': 32, 'filter_size': 5, 'strides': 1,
                                     'regularizer': 'l2_regularizer'}),
                (plx.layers.MaxPool2d, {'kernel_size': 2}),
                (plx.layers.Conv2d, {'num_filter': 64, 'filter_size': 5,
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
        'pipeline_config': {'name': 'train', 'batch_size': 64, 'num_epochs': None,
                            'shuffle': False},
        'x': X['train'],
        'y': y['train']
    },
    'eval_input_data_config': {
        'input_type': plx.configs.InputDataConfig.NUMPY,
        'pipeline_config': {'name': 'eval', 'batch_size': 32, 'num_epochs': None,
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

## Creating a distributed experiment

```python
def create_experiment(task_type, task_index=0):

    def graph_fn(mode, inputs):
        x = plx.layers.FullyConnected(mode, num_units=32, activation='tanh')(inputs['X'])
        return plx.layers.FullyConnected(mode, num_units=1, activation='sigmoid')(x)

    def model_fn(features, labels, mode):
        model = plx.models.Regressor(
            mode, graph_fn=graph_fn, loss_config=plx.configs.LossConfig(module='absolute_difference'),
            optimizer_config=plx.configs.OptimizerConfig(module='sgd', learning_rate=0.5, decay_type='exponential_decay', decay_steps=10),
            summaries='all', name='xor')
        return model(features, labels)

    os.environ['task_type'] = task_type
    os.environ['task_index'] = str(task_index)

    cluster_config = {
            'master': ['127.0.0.1:9000'],
            'ps': ['127.0.0.1:9001'],
            'worker': ['127.0.0.1:9002'],
            'environment': 'cloud'
        }

    config = plx.configs.RunConfig(cluster_config=cluster_config)

    estimator = plx.estimators.Estimator(model_fn=model_fn, model_dir="/tmp/polyaxon_logs/xor", config=config)

    return plx.experiments.Experiment(estimator, input_fn, input_fn)
```

# Installation

To install the latest version of Polyaxon: `pip install polyaxon`

Alternatively, you can also install from source by running (from source folder): `python setup.py install`

Or you can just clone the repo `git clone https://github.com/polyaxon/polyaxon.git`, and use the commands to do everything in docker:
 
 * `cmd/rebuild` to build the docker containers.
 * `cmd/py` to start a python3 shell with all requirements installed.
 * `cmd/jupyter` to start a jupyter notebook server.
 * `cmd/tensorboard` to start a tensorboard server.
 * `cmd/test` to run the tests.   

# Examples

Some example are provided [here](examples), more examples and use case will pushed, a contribution with an example is also appreciated.

# Project status

Polyaxon is in a pre-release "alpha" state. All interfaces, programming interfaces, and data structures may be changed without prior notice. 
We'll do our best to communicate potentially disruptive changes.

# Contributions

Please follow the contribution guide line: *[Contribute to Polyaxon](CONTRIBUTING.md)*.

# License

MIT License

# Credit

This work is based and was inspired from different projects, `tensorflow.contrib.learn`, `keras`, `sonnet`, and `seq2seq`.
The idea behind creating this library is to provide a tool that allow engineers and researchers to develop and experiment with end to end solutions.

The choice of creating a new library was very important to have a complete control over the apis and future design decisions.
