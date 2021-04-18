---
title: "Optimization Engine"
sub_link: "optimization-engine"
meta_title: "Polyaxon Optimization Engine Specification - Polyaxon References"
meta_description: "Finding good hyperparameters can be very challenging,
and requires to efficiently search the space of possible hyperparameters as well as
how to manage, schedule, and monitor a large set of experiments for hyperparameter tuning, Polyaxon Optimization Engine tries to simplify this by exposing a set of search algorithms."
visibility: public
status: published
is_index: true
tags:
  - reference
  - polyaxon
  - experimentation
  - hyperparameter-optimization
sidebar: "automation"
---

## Overview

Hyperparameters selection is crucial for creating robust models,
since they heavily influence the behavior of the learned model.
Finding good hyperparameters can be very challenging,
and requires to efficiently search the space of possible hyperparameters as well as
how to manage, schedule, and monitor a large set of experiments for hyperparameter tuning,

The way Polyaxon performs hyperparameter tuning is by providing a selection of customizable search algorithms.
Polyaxon supports both simple approaches such as `random search` and `grid search`, and provides a simple interface for
advanced approaches, such as `Hyperband` and `Bayesian Optimization`, it also integrates with tools such as `Hyperopt`,
and provides an interface for running custom iterative processes.

All these search algorithms run in an asynchronous way, and support concurrency and routing to leverage your cluster(s)'s resources to the maximum.

Some of these approaches are also iterative and improve based on previous experiments.

## Features

 * Easy-to-use: Polyaxon's Optimization Engine is a built-in service and can be used easily by adding a `matrix` section to your operations, you can run hyperparameter tuning using the CLI, client and the dashboard.
 * Scalability: Tuning hyperparameters or neural architectures requires leveraging a large amount of computation resources, using Polyaxon you can run hundreds of trials in parallel and intuitively track their progress.
 * Flexibility: Besides the rich built-in algorithms, Polyaxon allows users to customize various hyperparameter tuning algorithms, neural architecture search algorithms, early stopping algorithms, etc.
 * Efficiency: We are intensively working on more efficient model tuning from both system level and algorithm level. For example, leveraging early feedback to speedup tuning procedure.
 * Agnostic: The interface that we provide is agnostic to the framework, and even the language, used to define the model or function to optimize, hence you can use any machine learning framework, including PyTorch, XGBoost, MXNet, Tensorflow, and Keras.
 * Visualization and Dashboards: Polyaxon's Optimization Engine reuses the same logic and core features for jobs, tracking, checkpoints management, and integration with TensorBoard.

## Workflow

 * Define a search space.
 * Define a search algorithm.
 * Define a model to optimize.
 * Optionally define the queuing, routing, concurrency, and early stopping.

## Algorithms

In order to search a hyperparameter space, all search algorithms require a `matrix` section,
they also share some subsections such as: `params` definition of hyperparameters, `earlyStopping`, and `concurrency`.
Each one of these algorithms has a dedicated subsection to define the required options.

 * [Grid search](/docs/automation/optimization-engine/grid-search/)
 * [Random search](/docs/automation/optimization-engine/random-search/)
 * [Hyperband](/docs/automation/optimization-engine/hyperband/)
 * [Bayesian Optimization](/docs/automation/optimization-engine/bayesian-optimization/)
 * [Hyperopt](/docs/automation/optimization-engine/bayesian-optimization/)
 * [Custom iterative Optimization](/docs/automation/optimization-engine/iterative/)

## Pipeline helpers

All optimization algorithms can leverage the [pipeline helpers](/docs/automation/helpers/) for managing concurrency, early stopping, caching, ...

## Search Space

In order to define a search space, users must define how to generate the values that will be used to create
the parameters combination for running the component, The `params` are defined as `{key: value}`
object where the key is the name of the parameter you are defining and the value is one of these options:

### Discrete params

 * **choice**
 * **range**
 * **logspace**
 * **linspace**
 * **geomspace**

### Distributions params

 * **pchoice**
 * **uniform**
 * **quniform**
 * **loguniform**
 * **qloguniform**
 * **normal**
 * **qnormal**
 * **lognormal**
 * **qlognormal**

You can check all the options available in the [params section reference](/docs/automation/optimization-engine/params/).

Example usage

```yaml
matrix:
  kind: random
  params:
      lr:
        kind: logspace
        value: 0.01:0.1:5

      loss:
        kind: choice
        value: [MeanSquaredError, AbsoluteDifference]
```

These values can be accessed in the following way:

```yaml
--lr={{ lr }} --loss={{ loss }}
```
