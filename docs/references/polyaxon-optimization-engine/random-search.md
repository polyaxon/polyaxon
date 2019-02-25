---
title: "Random Search"
sub_link: "polyaxon-optimization-engine/random-search"
meta_title: "Polyaxon Optimization Engine - Random Search Specification - Polyaxon References"
meta_description: "Random search creates a number of unique experiments by sampling randomly from a search space. Random search is a competitive method for black-box parameter tuning in machine learning."
visibility: public
status: published
tags:
    - reference
    - polyaxon
    - experimentation
    - hyperparams-optimization
sidebar: "polyaxon-optimization-engine"
---

![random-search](../../../content/images/references/optimization-engine/random-search.png)

## Overview

Random search creates a number of unique experiments by sampling randomly from a search space. 

Random search is a competitive method for black-box parameter tuning in machine learning.

Random search requires a parameter `n_experiments`, this is essential because Polyaxon needs to know how many experiments to sample.

## Example

Here's an example of a random search in Polyaxon

```yaml
version: 1

kind: group

declarations:
  batch_size: 128

hptuning:

  random_search:
    n_experiments: 40

  matrix:
    lr:
      logspace: 0.01:0.1:5
    dropout:
      values: [0.2, 0.5]
    activation:
      pvalues: [[elu, 0.1], [relu, 0.2], [sigmoid, 0.7]]
    param1:
      uniform: [0, 1]

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn

run:
  cmd: python3 train.py --batch-size={{ batch_size }} \
                        --lr={{ lr }} \
                        --dropout={{ dropout }} \
                        --activation={{ activation }} \
                        --param1={{ param1 }}
```

In this example the random search algorithm will try 40 unique experiments based on the space search defined in the matrix subsection. The experiments will run sequentially.


## Concurrency

The previous example will run all experiments sequentially, this could be enough if the search space is small and/or we have very limited compute resources, 
but in many case, users will want to run experiments in parallel to traverse the search space quickly and take advantage of their compute resources:


```yaml
version: 1

kind: group

declarations:
  batch_size: 128

hptuning:
  concurrency: 5
  
  random_search:
    n_experiments: 40

  matrix:
    lr:
      logspace: 0.01:0.1:5
    dropout:
      values: [0.2, 0.5]
    activation:
      pvalues: [[elu, 0.1], [relu, 0.2], [sigmoid, 0.7]]
    param1:
      uniform: [0, 1]

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn

run:
  cmd: python3 train.py --batch-size={{ batch_size }} \
                        --lr={{ lr }} \
                        --dropout={{ dropout }} \
                        --activation={{ activation }} \
                        --param1={{ param1 }}
```

The updated example will create 40 experiments and start 5 concurrently, every time an experiment is finished, the algorithm will start a new one to keep the number of running experiments 5.


## Early stopping

Random search algorithm can be used with early stopping, to prevent the algorithm from starting all experiments in the search space:

```yaml
version: 1

kind: group

declarations:
  batch_size: 128

hptuning:
  concurrency: 5
  
  random_search:
    n_experiments: 40

  matrix:
    lr:
      logspace: 0.01:0.1:5
    dropout:
      values: [0.2, 0.5]
    activation:
      pvalues: [[elu, 0.1], [relu, 0.2], [sigmoid, 0.7]]
    param1:
      uniform: [0, 1]

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
  cmd: python3 train.py --batch-size={{ batch_size }} \
                        --lr={{ lr }} \
                        --dropout={{ dropout }} \
                        --activation={{ activation }} \
                        --param1={{ param1 }}
```

With this updated example, if one of the experiments reaches an accuracy of 0.9 or higher, or a loss of 0.05 or lower, the search algorithm will stop other running experiments, 
and any other experiments that is scheduled to be running.
