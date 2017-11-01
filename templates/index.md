[![Build Status](https://travis-ci.org/polyaxon/polyaxon.svg?branch=master)](https://travis-ci.org/polyaxon/polyaxon)
[![PyPI version](https://badge.fury.io/py/polyaxon.svg)](https://badge.fury.io/py/polyaxon)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/polyaxon/polyaxon)

# Polyaxon

Deep Learning and Reinforcement learning library for for building, training and monitoring models and experiments at any scale.

# Design Goals

Polyaxon is a set of tools to help simplify building and training deep learning models.

Polyaxon was built with the following goals:

 * Usability: Training a model should be easy enough, and should enable quick experimentations.
 
 * Scale: Experiments running locally, on premise, or on the cloud.
 
 * Concurrency: hyperparameter search and optimization in a concurrent way. 

 * Configurable: Models and experiments could be created using YAML files and/or a Python environment.

 * Extensibility: The modularity and the extensive documentation of the code makes it easy to build and extend the set of provided modules.

 * Monitoring: Polyaxon tracks experiments for comparison and reproducibility.
 

# Quick start

## A simple linear regression

```python
from polyaxon_schemas.losses import MeanSquaredErrorConfig
from polyaxon_schemas.optimizers import SGDConfig

import polyaxon as plx 

X = np.linspace(-1, 1, 100)
y = 2 * X + np.random.randn(*X.shape) * 0.33

# Test a data set
X_val = np.linspace(1, 1.5, 10)
y_val = 2 * X_val + np.random.randn(*X_val.shape) * 0.33


def graph_fn(mode, inputs):
    return plx.layers.Dense(units=1,)(inputs['X'])


def model_fn(features, labels, mode):
    model = plx.models.Regressor(
        mode, 
        graph_fn=graph_fn, 
        loss=MeanSquaredErrorConfig(),
        optimizer=SGDConfig(learning_rate=0.009),
        summaries='all', 
        name='regressor')
    return model(features, labels)


estimator = plx.estimators.Estimator(model_fn=model_fn, model_dir="/tmp/polyaxon_logs/linear")

estimator.train(input_fn=numpy_input_fn(
    {'X': X}, y, shuffle=False, num_epochs=10000, batch_size=len(X)))
```


## A reinforcement learning problem

```python
from polyaxon_schemas.losses import HuberLossConfig
from polyaxon_schemas.optimizers import SGDConfig
from polyaxon_schemas.rl.explorations import DecayExplorationConfig

import polyaxon as plx

env = plx.envs.GymEnvironment('CartPole-v0')

def graph_fn(mode, features):
    return plx.layers.Dense(units=512)(features['state'])

def model_fn(features, labels, mode):
    model = plx.models.DDQNModel(
        mode,
        graph_fn=graph_fn,
        loss=HuberLossConfig(),
        num_states=env.num_states,
        num_actions=env.num_actions,
        optimizer=SGDConfig(learning_rate=0.01),
        exploration_config=DecayExplorationConfig(),
        target_update_frequency=10,
        summaries='all')
    return model(features, labels)

memory = plx.rl.memories.Memory()
agent = plx.estimators.Agent(
    model_fn=model_fn, memory=memory, model_dir="/tmp/polyaxon_logs/ddqn_cartpole")

agent.train(env)
```


## A classification problem

```python
import tensorflow as tf
import polyaxon as plx

from polyaxon_schemas.optimizers import AdamConfig
from polyaxon_schemas.losses import SigmoidCrossEntropyConfig
from polyaxon_schemas.metrics import AccuracyConfig


def graph_fn(mode, features):
    x = plx.layers.Conv2D(filters=32, kernel_size=5)(features['image'])
    x = plx.layers.MaxPooling2D(pool_size=2)(x)
    x = plx.layers.Conv2D(filters=64, kernel_size=5)(x)
    x = plx.layers.MaxPooling2D(pool_size=2)(x)
    x = plx.layers.Flatten()(x)
    x = plx.layers.Dense(units=10)(x)
    return x


def model_fn(features, labels, params, mode, config):
    model = plx.models.Classifier(
        mode=mode,
        graph_fn=graph_fn,
        loss=SigmoidCrossEntropyConfig(),
        optimizer=AdamConfig(
            learning_rate=0.007, decay_type='exponential_decay', decay_rate=0.1),
        metrics=[AccuracyConfig()],
        summaries='all',
        one_hot_encode=True,
        n_classes=10)
    return model(features=features, labels=labels, params=params, config=config)


def experiment_fn(output_dir):
    """Creates an experiment using Lenet network.

    Links:
        * http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf
    """
    dataset_dir = '../data/mnist'
    plx.datasets.mnist.prepare(dataset_dir)
    train_input_fn, eval_input_fn = plx.datasets.mnist.create_input_fn(dataset_dir)

    experiment = plx.experiments.Experiment(
        estimator=plx.estimators.Estimator(model_fn=model_fn, model_dir=output_dir),
        train_input_fn=train_input_fn,
        eval_input_fn=eval_input_fn,
        train_steps=10000,
        eval_steps=10)

    return experiment


def main(*args):
    plx.experiments.run_experiment(experiment_fn=experiment_fn,
                                   output_dir="/tmp/polyaxon_logs/lenet",
                                   schedule='continuous_train_and_eval')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
```

## A regression problem

```python    
from polyaxon_schemas.losses import MeanSquaredErrorConfig
from polyaxon_schemas.metrics import (
    RootMeanSquaredErrorConfig,
    MeanAbsoluteErrorConfig,
)
from polyaxon_schemas.optimizers import AdagradConfig

import polyaxon as plx

NUM_RNN_LAYERS = 2
NUM_RNN_UNITS = 2

def graph_fn(mode, features):
    x = features['x']
    for i in range(NUM_LAYERS):
        x = plx.layers.LSTM(units=NUM_RNN_UNITS)(x)
    return plx.layers.Dense(units=1)(x)

def model_fn(features, labels, mode):
    return plx.models.Regressor(
        mode=mode,
        graph_fn=graph_fn,
        loss=MeanSquaredErrorConfig(),
        optimizer=AdagradConfig(learning_rate=0.1),
        metrics=[
            RootMeanSquaredErrorConfig(),
            MeanAbsoluteErrorConfig()
        ]
    )(features=features, labels=labels)

xp = plx.experiments.Experiment(
        estimator=plx.estimators.Estimator(model_fn=model_fn, model_dir=output_dir),
        train_input_fn=plx.processing.numpy_input_fn(
            x={'x': x['train']}, y=y['train'], batch_size=64, num_epochs=None, shuffle=False),
        eval_input_fn=plx.processing.numpy_input_fn(
            x={'x': x['train']}, y=y['train'], batch_size=32, num_epochs=None, shuffle=False),
        train_steps=train_steps,
        eval_steps=10)
xp.continuous_train_and_evaluate()
```

## Creating a distributed experiment

```python

import numpy as np
import tensorflow as tf
from polyaxon_schemas.settings import RunConfig, ClusterConfig

import polyaxon as plx

from polyaxon_schemas.losses import AbsoluteDifferenceConfig
from polyaxon_schemas.optimizers import SGDConfig

tf.logging.set_verbosity(tf.logging.INFO)


def create_experiment(task_type, task_id=0):
    def graph_fn(mode, features):
        x = plx.layers.Dense(units=32, activation='tanh')(features['X'])
        return plx.layers.Dense(units=1, activation='sigmoid')(x)

    def model_fn(features, labels, mode):
        model = plx.models.Regressor(
            mode, graph_fn=graph_fn,
            loss=AbsoluteDifferenceConfig(),
            optimizer=SGDConfig(learning_rate=0.5,
                                decay_type='exponential_decay',
                                decay_steps=10),
            summaries='all', name='xor')
        return model(features, labels)

    config = RunConfig(cluster=ClusterConfig(master=['127.0.0.1:9000'],
                                             worker=['127.0.0.1:9002'],
                                             ps=['127.0.0.1:9001']))

    config = plx.estimators.RunConfig.from_config(config)
    config = config.replace(task_type=task_type, task_id=task_id)

    est = plx.estimators.Estimator(model_fn=model_fn, model_dir="/tmp/polyaxon_logs/xor",
                                   config=config)

    # Data
    x = np.asarray([[0., 0.], [0., 1.], [1., 0.], [1., 1.]], dtype=np.float32)
    y = np.asarray([[0], [1], [1], [0]], dtype=np.float32)

    def input_fn(num_epochs=1):
        return plx.processing.numpy_input_fn({'X': x}, y,
                                             shuffle=False,
                                             num_epochs=num_epochs,
                                             batch_size=len(x))

    return plx.experiments.Experiment(est, input_fn(10000), input_fn(100))


# >> create_experiment('master').train_and_evaluate()
# >> create_experiment('worker').train()
# >> create_experiment('ps').run_std_server()
```

## Creating concurrent experiments in kubernetes clusters based on a yaml file

```yaml

---
version: 1

project:
  name: conv_mnsit

matrix:
  lr:
    logspace: 0.01:0.1:2

settings:
  logging:
    level: INFO
  run_type: kubernetes

environment:
  delay_workers_by_global_step: true
  n_workers: 5
  n_ps: 3
  run_config:
    save_summary_steps: 100
    save_checkpoints_steps: 100

model:
  classifier:
    loss:
      SigmoidCrossEntropy:
    optimizer:
      Adam:
        learning_rate: "{{ lr }}"
    metrics:
      - Accuracy
      - Precision
    one_hot_encode: true
    n_classes: 10
    graph:
      input_layers: image
      layers:
        - Conv2D:
            filters: 32
            kernel_size: 3
            strides: 1
            activation: elu
            regularizer:
                L2:
                  l: 0.02
        - MaxPooling2D:
            pool_size: 2
        - Conv2D:
            filters: 64
            kernel_size: 3
            activation: relu
            regularizer:
                L2:
                  l: 0.02
        - MaxPooling2D:
            pool_size: 2
        - Flatten:
        - Dense:
            units: 128
            activation: tanh
        - Dropout:
            rate: 0.8
        - Dense:
            units: 256
            activation: tanh
        - Dropout:
            rate: 0.8
        - Dense:
            units: 10

train:
  train_steps: 100
  data_pipeline:
    TFRecordImagePipeline:
      batch_size: 64
      num_epochs: 5
      shuffle: true
      data_files: ["../data/mnist/mnist_train.tfrecord"]
      meta_data_file: "../data/mnist/meta_data.json"
      feature_processors:
        image:
          input_layers: [image]
          layers:
            - Cast:
                dtype: float32

eval:
  data_pipeline:
    TFRecordImagePipeline:
      batch_size: 32
      num_epochs: 1
      shuffle: False
      data_files: ["../data/mnist/mnist_eval.tfrecord"]
      meta_data_file: "../data/mnist/meta_data.json"
      feature_processors:
        image:
          input_layers: [image]
          layers:
            - Cast:
                dtype: float32

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

Some examples are provided [here](examples), more examples and use cases will pushed, a contribution with an example is also appreciated.

# Project status

Polyaxon is in a pre-release "alpha" state. All interfaces, programming interfaces, and data structures may be changed without prior notice. 
We'll do our best to communicate potentially disruptive changes.

# Contributions

Please follow the contribution guide line: *[Contribute to Polyaxon](CONTRIBUTING.md)*.

# License

MIT License

# Credit

This work is based and was inspired from different projects, `tensorflow.contrib.learn`, `keras`, `sonnet`, `seq2seq` and many other great open source projects, see [ACKNOWLEDGEMENTS](ACKNOWLEDGEMENTS).

The idea behind creating this library is to provide a tool that allow engineers and researchers to develop and experiment with end to end solutions.

The choice of creating a new library was very important to have a complete control over the apis and future design decisions.
