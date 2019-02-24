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

Random search requires a parameter `n_experiments`, this is essential because Polyaxon needs to know how many experiments to sample.

Here's an example of a

```yaml
---
version: 1

kind: group

declarations:
  batch_size: 128

hptuning:
  concurrency: 2

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
