---
title: "Grid Search"
sub_link: "polyaxon-optimization-engine/grid-search"
meta_title: "Polyaxon Optimization Engine - Grid Search Specification - Polyaxon References"
meta_description: "Grid Search is essentially an exhaustive search through a manually specified set of hyperparameters."
visibility: public
status: published
tags:
    - reference
    - polyaxon
    - experimentation
    - hyperparams-optimization
sidebar: "polyaxon-optimization-engine"
---

![grid-search](../../../content/images/references/optimization-engine/grid-search.png)

## Overview
 
The grid search is the default algorithm used by Polyaxon in case no other algorithm is defined.
and it accepts one optional parameter `n_experiments` in case the user does not want to traverse the whole space search.

Grid search is essentially an exhaustive search through a manually specified set of hyperparameters. The user can possibly limit the number of experiments created by providing n_experiments.

Grid search does not allow the use of distributions, and requires that all values of the matrix definition to be [discrete values](/references/polyaxonfile-yaml-specification/hptuning/#discrete-values).

## Example

Here's an example of a grid search in Polyaxon

```yaml
version: 1

kind: group

declarations:
  batch_size: 128

hptuning:
  matrix:
    lr:
      logspace: 0.01:0.1:5
    dropout:
      values: [0.2, 0.5]

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn

run:
  cmd: python3 train.py --batch-size={{ batch_size }} --lr={{ lr }} --dropout={{ dropout }}
```

Other possible matrix options that can be found [here](/references/polyaxonfile-yaml-specification/hptuning/#discrete-values).

This example will define 10 experiments based on the cartesian product of `lr` and `dropout` possible values.

## Maximum number of experiments

We can restrict the number of experiments to run by using `n_experiments`, the updated version:

```yaml
version: 1

kind: group

declarations:
  batch_size: 128

hptuning:
  grid_search:
    n_experiments: 4

  matrix:
    lr:
      logspace: 0.01:0.1:5
    dropout:
      values: [0.2, 0.5]

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn

run:
  cmd: python3 train.py --batch-size={{ batch_size }} --lr={{ lr }} --dropout={{ dropout }}
```

This updated example will create only 4 experiments from the total number of possible experiments.

## Concurrency

The previous example will run all experiments sequentially, this could be enough if the search space is small and/or we have very limited compute resources, 
but in many case, users will want to run experiments in parallel to traverse the search space quickly and take advantage of their compute resources:

```yaml
version: 1

kind: group

declarations:
  batch_size: 128

hptuning:
  
  concurrency: 4

  grid_search:
    n_experiments: 8

  matrix:
    lr:
      logspace: 0.01:0.1:5
    dropout:
      values: [0.2, 0.5]

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn

run:
  cmd: python3 train.py --batch-size={{ batch_size }} --lr={{ lr }} --dropout={{ dropout }}
```

The updated example will create 8 experiments and start 4 concurrently, every time an experiment is finished, the algorithm will start a new one to keep the number of running experiments 4. 

## Early stopping

Grid search algorithm can be used with early stopping, to prevent the algorithm from starting all experiments in the search space:

```yaml
version: 1

kind: group

declarations:
  batch_size: 128

hptuning:
  grid_search:
    n_experiments: 4

  matrix:
    lr:
      logspace: 0.01:0.1:5
    dropout:
      values: [0.2, 0.5]

  early_stopping:
    - metric: accuracy
      value: 0.9
      optimization: maximize
    - metric: loss
      value: 0.05
      optimization: minimize

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn

run:
  cmd: python3 train.py --batch-size={{ batch_size }} --lr={{ lr }} --dropout={{ dropout }}
```

With this updated example, if one of the experiments reaches an accuracy of 0.9 or higher, or a loss of 0.05 or lower, the search algorithm will stop other running experiments, 
and any other experiments that is scheduled to be running.
