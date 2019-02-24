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

The grid search is the default algorithm used by Polyaxon in case no other algorithm is defined.
and it accepts one optional parameter `n_experiments` in case the user does not want to traverse the whole space search.

The grid search does not allow the use of distribution, and requires that all matrix definition are values or ranges.

Here's an example of a

```yaml
---
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

Other possible matrix options that can be found [here](/references/polyaxonfile-yaml-specification/sections/#discrete-values).

The previous example will define 10 experiments based on the cartesian product of `lr` and `dropout` possible values.

We can restrict the number of experiments torun by using `n_experiments`,
the update version:


```yaml
---
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
