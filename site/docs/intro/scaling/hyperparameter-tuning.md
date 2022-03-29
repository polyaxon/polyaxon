---
title: "Hyperparameter Tuning"
sub_link: "scaling/hyperparameter-tuning"
meta_title: "Hyperparameter Tuning - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Hyperparameter Tuning - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

Polyaxon provides several features for running hyperparameter tuning.

## Overview

Oftentimes you may want to create many experiments with different parameters and automatically manage the execution.

In order to make this tutorial usable for all Polyaxon users, 
we will run several configurations in parallel using the **eager mode**, and we will use algorithms supported in all Polyaxon distributions:
 * Grid Search
 * Random Search

In order to run the commands in this section with the **eager mode**, you need to install Polyaxon with `numpy`:

```bash
pip install "polyaxon[numpy]"
```

> To run these commands without the eager mode, and have a fully automated pipeline managing the executions and controlling concurrency limits and early stopping conditions, you need to have access to Polyaxon EE or Polyaxon Cloud.

## Grid search

Let's run another polyaxonfile `hyperparams_grid.yaml`, which contains a hyperparameter tuning definition with grid seach algorithm, this is the content of the file:

```yaml
version: 1.1
kind: operation
matrix:
  kind: grid
  params:
    learning_rate:
      kind: linspace
      value: 0.001:0.1:5
    dropout:
      kind: choice
      value: [0.25, 0.3]
    conv_activation:
      kind: choice
      value: [relu, sigmoid]
    epochs:
      kind: choice
      value: [5, 10]
urlRef: https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/experimentation/typed.yaml
```

This is an operation based on the same component used in the previous quick-start guides.
Instead of defining a single set of params, similar to what we did in previous sections of this tutorial,
this file defines a matrix, in this case, with the grid search algorithm.

It uses the same component, Polyaxon validates the search space generated against
the inputs and outputs defined in the component.
It then generates multiple operations based on the search space anw it will manage their execution using a pipeline.

Running an operation with a hyperparameter tuning matrix is similar to any other operation:

```bash
polyaxon run --eager --url https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/optimization/hyperparams_grid.yaml
```

If you have cloned the quick-start repo, you can run:

```bash
polyaxon run --eager -f optimization/hyperparams_grid.yaml
```

Note that in both commands we are passing `--eager`. If you don't provide the `--eager` flag Polyaxon will:
 * Run the hyperparameter tuning pipeline in a managed mode if you have access to Polyaxon EE or Polyaxon Cloud.
 * Raise an exception if you are using Polyaxon CE.

> For more details check the [grid search reference](/docs/automation/optimization-engine/grid-search/)

You can also use the CLI to run this operation without creating a Polyaxonfile:

```bash
polyaxon run --url https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/experimentation/typed.yaml -HP learning_rate='linspace:[0.001,0.1,5]' -HP conv_activation='choice:[0.25, 0.3]' -HP dropout='choice:[relu, sigmoid]' -HP epochs='choice:[5, 10]'
```

Please make sure to add `--eager` if you are on Polyaxon CE. 

## Random search

The `hyperparams_random.yaml` polyaxonfile is similar to the grid search polyaxonfile, the only difference is that it defines a random search matrix section:

```yaml
version: 1.1
kind: operation
matrix:
  kind: random
  numRuns: 10
  params:
    learning_rate:
      kind: linspace
      value: 0.001:0.1:5
    dropout:
      kind: choice
      value: [0.25, 0.3]
    conv_activation:
      kind: pchoice
      value: [[relu, 0.1], [sigmoid, 0.8]]
    epochs:
      kind: choice
      value: [5, 10]
urlRef: https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/experimentation/typed.yaml
```

To run this polyaxonfile:

```bash
polyaxon run --eager --url https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/optimization/hyperparams_random.yaml
```

Random search also provides access to the continuous distributions in addition to the discrete distributions.

> For more details check the [random search reference](/docs/automation/optimization-engine/random-search/)

You can also use the CLI to run this operation without creating a Polyaxonfile:

```bash
polyaxon run --url https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/experimentation/typed.yaml --matrix-kind random --matrix-num-runs 10 -HP learning_rate='linspace:[0.001,0.1,5]' -HP conv_activation='choice:[0.25, 0.3]' -HP dropout='choice:[relu, sigmoid]' -HP epochs='choice:[5, 10]'
```

Please make sure to add `--eager` if you are on Polyaxon CE.

## Learn More

Polyaxon provides several generators for defining a [search space](/docs/automation/optimization-engine/params/) and several
[search algorithms for hyperparameter tuning](/docs/automation/optimization-engine/).

For users with Polyaxon EE or Polyaxon Cloud access,
there are also tools to [control caching](/docs/automation/helpers/cache/) of executions with similar configurations,
and [concurrency](/docs/automation/helpers/concurrency/) for enforcing of parallelism.
Finally, every pipeline in Polyaxon can also define [early stopping strategies](/docs/automation/helpers/early-stopping/).

The repo contains more hyperparameter tuning examples in the automation folder.
