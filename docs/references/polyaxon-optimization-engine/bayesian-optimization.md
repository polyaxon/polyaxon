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

Bayesian optimization is an extremely powerful technique.
The main idea behind it is to compute a posterior distribution over the objective function based on the data,
and then select good points to try with respect to this distribution.

The way Polyaxon performs bayesian optimization is by measuring the expected increase in the maximum objective value
seen over all experiments in the group, given the next point we pick.

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


Example :


```yaml
...

hptuning:
  concurrency: 2
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

Example with early stopping:

```yaml
...

hptuning:
  concurrency: 2
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
