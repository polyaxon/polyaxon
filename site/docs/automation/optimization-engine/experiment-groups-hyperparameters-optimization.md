---
title: "Experiment Groups - Hyperparameters Optimization"
sub_link: "experiment-groups-hyperparameters-optimization"
meta_title: "Experiment Groups - Hyperparameters Optimization in Polyaxon - Core Concepts"
meta_description: "An Experiment Group is an automatic and practical way to run a version of your model and data with different hyper parameters."
tags:
  - concepts
  - polyaxon
  - experimentation
  - experiment-groups
  - architecture
  - experimentation
  - hyperparameter-optimization
sidebar: "core"
---

Assuming that you have already a [project](/concepts/projects/) created and initialized,
and you uploaded your code consisting of a single file `train.py` that accepts 2 parameters

  * learning rate `lr`
  * batch size `batch_size`

If you want to run this code with different learning rate  `lr` values,
you can use the [matrix section](/references/yaml-specification/hptuning/#matrix) to declare the values you want to run.

## Updating the polyaxonfile.yaml with a matrix

The first thing you need to do is to update the default `polyaxonfile.yaml` that was generated.

You need to set the required information, for example, if the code requires `tensorflow` and `sklearn`,
the polyaxonfile.yaml `build` section could look something like this

```yaml
...

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn

run:
  cmd: python3 train.py --batch-size={{ batch_size }} --lr={{ lr }}
```

This declares a section to run our `train.py` file by passing two values, the `learning rate` and the `batch_size`.

> For more details about the `run section` check the [run section reference](/references/yaml-specification/run/)

Now you need to declare these values, and for that you will add 2 more sections to the polyaxonfile.yaml

 * A [params section](/references/yaml-specification/params/), to declare a constant value for `batch_size`
 * A [hptuning section](/references/yaml-specification/hptuning/) with [matrix subsection](/references/yaml-specification/hptuning/#matrix), to declare the values for `lr`

The new `polyaxonfile.yaml` after the update

```yaml

---
version: 1

kind: group

params:
  batch_size: 128

hptuning:
  matrix:
    lr:
      logspace: 0.01:0.1:5

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn

run:
  cmd: python3 train.py --batch-size={{ batch_size }} --lr={{ lr }}
```

> The params section was not completely necessary, we could have also just passed the value directly `--batch-size=128`

So what we did is that we declared a constant value for `batch_size`, and a value for `lr` going from `0.01` to `0.1` with `5` steps spaced evenly on a `log scale`.

There are other options that we could have used such as

 * **values**: [value1, value2, value3, ...]
 * **pvalues**: [(value1, prob1), (value2, prob12), (value3, prob3), ...]
 * **range**: [start, stop, step]
 * **logspace**: [start, stop, step]
 * **linspace**: [start, stop, num]
 * **geomspace**: [start, stop, num]

And distributions, when using random search, hyperband, or bayesian optimization:

 * **uniform**: [low, high]
 * **quniform**: [low, high]
 * **loguniform**: [low, high]
 * **qloguniform**: [low, high]
 * **normal**: [loc, scale]
 * **qnormal**: [loc, scale]
 * **lognormal**: [loc, scale]
 * **qlognormal**: [loc, scale]

You can check all the options available in the [matrix section reference](/references/yaml-specification/hptuning/#matrix).

To make sure that the Polyaxon file is valid, and creates multiple values for `lr`, we can run the following

```bash
polyaxon check -f polyaxonfile.yaml --definition

Polyaxonfile valid

This polyaxon specification has experiment group with the following definition:
----------------  -----------------
Search algorithm  grid
Concurrency       2 concurrent runs
Early stopping    deactivated
----------------  -----------------
```

This command validate the polyaxonfile, and the option `-def` returns the group definition.

> For more details about this command please run `polyaxon check --help`, or check the [command reference](/docs/core/cli/check/)

> Polyaxon merges the combination values from matrix for a single experiment with the values from params and export under the environment variable name `POLYAXON_DECLARATIONS`.
> Check how you can [get the experiment params](/docs/experimentation/tracking/in-cluster/#hyperparams) to use them with your models.

## Running a group of experiments

To run this polyaxonfile execute

```bash
polyaxon run

Creating an experiment group with 5 experiments.

Experiment group was created
```

> For more details about this command please run `polyaxon run --help`, or check the [command reference](/docs/core/cli/run/)

Now one thing we did not discuss is how many experiments we want to run in parallel,
and how we want to perform the hyperparameters search. Be default, Polyaxon
will schedule your experiments sequentially and explore the space with the [grid search](/references/polyaxon-optimization-engine/grid-search/) algorithm.


## Running concurrent experiments

Now imagine we have enough resources on our cluster to run experiments in parallel.
And we want to run 2 experiments concurrently, and explore the space [randomly](/references/polyaxon-optimization-engine/random-search/) instead of sequentially.

Although we can modify the `polyaxonfile.yaml` to include this new section,
we will do something different this time and override this value with a new file, same way you would do with `docker/docker-compose`.

Create a new file, let's call it polyaxonfile_override.yaml

> You can call your Polyaxonfiles anything you want. By default, Polyaxon commands look for files called `polyaxonfile.yaml`.
> If you call your files differently or want to override values, you need to use the option `-f`

```bash
vi polyaxonfile_override.yaml
```

And past the following hptuning section.

```yaml
version: 1

hptuning:
  concurrency: 2
  random_search:
    n_experiments: 5
```

If we run again the `check` command with `-def` or `--definition` option, we will get

```bash
polyaxon check -f polyaxonfile.yaml -f polyaxonfile_override.yaml -x

This Polyaxon specification has experiment group with the following definition:
--------------------  -----------------
Search algorithm      random
Concurrency           2 concurrent runs
Early stopping        deactivated
Experiment to create  5
--------------------  -----------------
```

Let's run our new version

```bash
 polyaxon run -f polyaxonfile.yaml -f polyaxonfile_override.yaml

Creating an experiment group with 5 experiments.

Experiment group was created
```

## Maximum number of experiments

Sometimes you don't wish to explore the matrix space exhaustively.
In that case, you can define a maximum number of experiments to explore from the matrix space.
The value must be of course less than the total number of experiments in the matrix space.

In order to activate this option, you must update your polyaxonfile's `hptuning` section with `n_experiments`


```yaml

---
version: 1

hptuning:
  concurrency: 2
  grid_search:
    n_experiments: 4
```

This will create a maximum of 4 experiments in this group independently of how big is the total number of experiments in matrix space.

## Early stopping

Another way to stop the search algorithm is to provide a condition for early stopping.
Obviously in this case, early stopping is only responsible for the number of experiments to run.
For an early stopping related to the number of steps or epochs, you should be able to provide such logic in your code.

In order to activate this option, you must update your polyaxonfile's `hptuning` section with `early_stopping`

```yaml
version: 1

hptuning:
  concurrency: 2
  random_search:
    n_experiments: 4
  early_stopping:
    - metric: accuracy
      value: 0.9
      optimization: maximize
    - metric: loss
      value: 0.05
      optimization: minimize
```

In this case, the scheduler will not start any more experiments, if one of the experiments in the group validate the following condition:

 * An accuracy >= 0.9
 * Or a loss <= 0.05

## Checking the status of your experiments

First, we can double check that our groups were created.

For that, you can use the Polyaxon dashboard or Polyaxon CLI.

```bash
polyaxon project groups

Experiment groups for project `admin/mnist`.


Navigation:

-----  -
count  2
-----  -

Experiment groups:

  id  unique_name    project_name    created_at           concurrency    num_experiments    num_pending_experiments    num_running_experiments
----  -------------  --------------  -----------------  -------------  -----------------  -------------------------  -------------------------
   1  admin.mnist.1  admin.mnist     a few seconds ago              1                  5                          4                          1
   2  admin.mnist.2  admin.mnist     a few seconds ago              2                  5                          3                          2
```

We can see that we created 2 groups, the first one with sequential runs, and the second one with 2 concurrent runs.

We can also see how many experiments are running/pending now.

We can have a look at the two experiments running concurrently in the second group.

Again you can go to the Polyaxon dashboard or use the Polyaxon CLI.

```bash
polyaxon group -g 2 experiments

Experiments for experiment group `2`.


Navigation:

-----  -
count  5
-----  -

Experiments:

  id  unique_name       user    last_status    created_at         is_clone      num_jobs  finished_at    started_at
----  ----------------  ------  -------------  -----------------  ----------  ----------  -------------  -----------------
   6  admin.mnist.2.6   admin   Created        a few seconds ago  False                0
   7  admin.mnist.2.7   admin   Created        a few seconds ago  False                0
   8  admin.mnist.2.8   admin   Starting       a few seconds ago  False                0                 a few seconds ago
   9  admin.mnist.2.9   admin   Created        a few seconds ago  False                0
  10  admin.mnist.2.10  admin   Building       a few seconds ago  False                0                 a few seconds ago
```

## Experiment group search algorithms

In these introductory sections we demonstrated how to conduct hyperparameter tuning with 2 algorithms;
[grid search](/references/polyaxon-optimization-engine/grid-search/) and [random search](/references/polyaxon-optimization-engine/random-search/).

Sometimes you might have a large search space where you want to use advanced search algorithms.
Polyaxon supports, in addition to [grid search](/references/polyaxon-optimization-engine/grid-search/) and [random search](/references/polyaxon-optimization-engine/random-search/),
[Hyperband](/references/polyaxon-optimization-engine/hyperband/) and [Bayesian Optimization](/references/polyaxon-optimization-engine/bayesian-optimization/).

For more information on hyperparameter tuning and optimization please go to [Optimization Engine Reference](/references/polyaxon-optimization-engine/).


> For more details about this command please run `polyaxon group --help`, or check the [command reference](/docs/core/cli/run/)


To check the logs, resources, jobs, and statuses of a specific experiment, please go to [experiments](/concepts/experiments/).
The section also covers how to customize the resources of an experiment, the configuration,
the log level and many important information.

All the information that you will learn in that section applies to experiment groups,
because groups are only a collection of experiments.

In the experiments section, you will also see how you can execute a single experiment without concurrency.
