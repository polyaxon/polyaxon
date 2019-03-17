---
title: "Hyperband"
sub_link: "polyaxon-optimization-engine/hyperband"
meta_title: "Polyaxon Optimization Engine - Grid Search Specification - Polyaxon References"
meta_description: "Hyperband is a relatively new method for tuning iterative algorithms. It performs random sampling and attempts to gain an edge by using time spent optimizing in the best way. The algorithm tries a large number of random configurations/experiments, then decides which configurations to keep based on their progress."
visibility: public
status: published
tags:
    - reference
    - polyaxon
    - experimentation
    - hyperparams-optimization
sidebar: "polyaxon-optimization-engine"
---

![hyperband](../../../content/images/references/optimization-engine/hyperband.png)

## Overview 

Hyperband is a relatively new method for tuning iterative algorithms.
It performs random sampling and attempts to gain an edge by using time spent optimizing in the best way.

The algorithm tries a large number of random configurations/experiments, then decides which configurations to keep based on their progress.

The Hyperband is implemented, is that it creates several buckets, each bucket has a number of randomly generated hyperparameter configurations, 
each configuration uses a resource (e.g. number of steps, number of epochs, batch size, ...). To adapt the algorithms maximum resource allocation, users can use `num_iter`.

After trying a number of configurations, it chooses top `number of observation/eta` configurations and runs them using increased `resource*eta` resource. 
At last, it chooses the best configuration it has found so far.


## Configuration

In order to configure this search algorithm correctly, you need to have as one of the hyperparameters,
a resource, this could be the number of steps or epochs, and a metric that you want to maximize or minimize.
You can also indicate if the experiments should be restarted from scratch or resumed from the last check point.

The way Hyperband works is by discarding poor performing
configurations leaving more resources for more promising configurations during the successive halving.

In order to use Hyperband correctly, you must define a metric called `resource` that the algorithm
will increase iteratively. Here's an example of resource definitions:

```yaml
resource:
  name: num_steps
  type: int
```

You can also have a resource with type float.

Another important concept is the metric to optimize, for example:

```yaml
metric:
  name: loss
  optimization: minimize
```

or

```yaml
metric:
  name: accuracy
  optimization: maximize
```

## Example

A complete definition of the hptuning section:

```yaml
...

hptuning:
  concurrency: 5

  hyperband:
    max_iter: 81
    eta: 3
    resource:
      name: num_steps
      type: int
    metric:
      name: loss
      optimization: minimize
    resume: False

  matrix:
    learning_rate:
      uniform: [0, 0.9]
    dropout:
      values: [0.25, 0.3]
    activation:
      pvalues: [[relu, 0.1], [sigmoid, 0.8]]
```

In this example we allocate a maximum resources of `81`, our resource in this case is the `num_steps` which is of type `int` that we pass to our model.

This is how the algorithm works with this config:


|              | bucket=4                    | bucket=3                     | bucket=2                     | bucket=1                     | bucket=0                    |
|--------------|-----------------------------|------------------------------|------------------------------|------------------------------|-----------------------------|
|iteration     |num configs   resource alloc |num configs   resource alloc  |num configs   resource alloc  |num configs   resource alloc  |num configs   resource alloc |
|0             |81             1             |27                          3 |9              9              |6              27             |5                          81|
|1             |27             3             |9                          9  |3              27             |2              81             |                             |
|2             |9             9              |3                          27 |1              81             |                              |                             |
|3             |3             27             |1                          81 |                              |                              |                             |
|4             |1             81             |                              |                              |                              |                             |

## Concurrency

It's recommended to run Hyperband with concurrency because the algorithms starts with a large number of experiments, otherwise all experiments will run sequentially.

## Early stopping

Hyperband algorithm can be used with early stopping, to prevent the algorithm from starting all experiments in the search space:


```yaml
...

hptuning:
  concurrency: 5

  hyperband:
    max_iter: 81
    eta: 3
    resource:
      name: num_steps
      type: int
    metric:
      name: loss
      optimization: minimize
    resume: False

  matrix:
    learning_rate:
      uniform: [0, 0.9]
    dropout:
      values: [0.25, 0.3]
    activation:
      pvalues: [[relu, 0.1], [sigmoid, 0.8]]

  early_stopping:
    - metric: accuracy
      value: 0.9
      optimization: maximize
    - metric: loss
      value: 0.05
      optimization: minimize
```

With this updated example, if one of the experiments reaches an accuracy of 0.9 or higher, or a loss of 0.05 or lower, the search algorithm will stop other ru ng experiments, 
and any other experiments that is scheduled to be running.
