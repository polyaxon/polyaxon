---
title: "Bayesian Optimization"
sub_link: "polyaxon-optimization-engine/bayesian-optimization"
meta_title: "Polyaxon Optimization Engine - Bayesian Optimization Specification - Polyaxon References"
meta_description: "Bayesian optimization is an extremely powerful technique. The main idea behind it is to compute a posterior distribution over the objective function based on the data, and then select good points to try with respect to this distribution. 
The way Polyaxon performs bayesian optimization is by measuring the expected increase in the maximum objective value seen over all experiments in the group, given the next point we pick."
visibility: public
status: published
tags:
    - reference
    - polyaxon
    - experimentation
    - hyperparams-optimization
sidebar: "polyaxon-optimization-engine"
---

![bayesian-optimization](../../../content/images/references/optimization-engine/bayesian-optimization.png)

## Overview 

Bayesian optimization is an extremely powerful technique.
The main idea behind it is to compute a posterior distribution over the objective function based on the data,
and then select good points to try with respect to this distribution.

The way Polyaxon performs bayesian optimization is by measuring the expected increase in the maximum objective value
seen over all experiments in the group, given the next point we pick.

## Configuration

Since the bayesian optimization leverages previous experiments, the algorithm requires a metric to optimize (`maximize` or `minimize`).

To use bayesian optimization the user must define a utility function. This utility defines what acquisition function and bayesian process to use.

### Acquisition functions

A couple of acquisition functions can be used: `ucb`, `ei` or `poi`.

  * `ucb`: Upper Confidence Bound,
  * `ei`: Expected Improvement
  * `poi`: Probability of Improvement

When using `ucb` as acquisition function, a tunable parameter `kappa` is also required, to balance exploitation
against exploration, increasing kappa will make the optimized hyperparameters pursuing exploration.

When using `ei` or `poi` as acquisition function, a tunable parameter `eps` is also required,
to balance exploitation against exploration, increasing epsilon will
make the optimized hyperparameters are more spread out across the whole range.

### Gaussian process

Polyaxon allows to tune the gaussian process.

 * `kernel`: `matern` or `rbf`.
 * `length_scale`: float
 * `nu`: float
 * `n_restarts_optimizer`: int


### Number of Initial Trials

In order for the algorithm to function correctly, an initial iteration of random experiments is required to create a seed of observations.

This initial random results are used by the algorithm to update the regression model for generating the next suggestions.

```yaml
n_initial_trials: 40
```

This configuration will create 40 random experiments, before start suggestion new experiments.

### Number of iterations 

After creating the first set of random observations, the algorithm will use these results to update the regression model and suggest a new experiment to run.

Every time an experiment is done, the results are used as an observation and are appended to the historical values so that the algorithm can use all the observations again to suggest more experiments to run.

The algorithm will keep suggesting more experiments and adding their results as an observation, every time we make a new observation, 
i.e. an experiment finishes and reports results to the platform, the results are append to the historical values, and then used to make a better suggestion.

```yaml
n_iterations: 15
```

This configuration will make 15 suggestions based on the historical values, every time an observation is made is appended to the historical values to make better subsequent suggestions. 

## Example


```yaml
...

hptuning:
  concurrency: 5
  bo:
    n_iterations: 15
    n_initial_trials: 30
    metric:
      name: loss
      optimization: minimize
    utility_function:
      acquisition_function: ucb
      kappa: 1.2
      gaussian_process:
        kernel: matern
        length_scale: 1.0
        nu: 1.9
        n_restarts_optimizer: 0

  matrix:
    learning_rate:
      uniform: [0, 0.9]
    dropout:
      values: [0.25, 0.3]
    activation:
      pvalues: [[relu, 0.1], [sigmoid, 0.8]]
```

## Concurrency

Bayesian Optimization algorithm uses concurrency to run all the initial number of experiments in parallel, if not provided they will run sequentially. 
And after that, every iteration will result in one new suggestion.

## Early stopping

Bayesian Optimization algorithm can be used with early stopping, to prevent the algorithm from starting all experiments in the initial step but also at every subsequent iteration: 

```yaml
...

hptuning:
  concurrency: 5
  bo:
    n_iterations: 15
    n_initial_trials: 30
    metric:
      name: loss
      optimization: minimize
    utility_function:
      acquisition_function: ei
      eps: 1.2
      gaussian_process:
        kernel: rbf
        length_scale: 1.0
        nu: 1.9
        n_restarts_optimizer: 0

  matrix:
    learning_rate:
      uniform: [0.001, 0.09]
    dropout:
      values: [0.25, 0.3]
    activation:
      values: [relu, sigmoid]

  early_stopping:
    - metric: accuracy
      value: 0.9
      optimization: maximize
    - metric: loss
      value: 0.05
      optimization: minimize
```

With this updated example, if one of the experiments reaches an accuracy of 0.9 or higher, or a loss of 0.05 or lower, the search algorithm will stop other running experiments, 
and any other experiments that is scheduled to be running.
