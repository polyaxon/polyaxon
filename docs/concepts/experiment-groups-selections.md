---
title: "Experiment Groups - Selections"
sub_link: "experiment-groups-selections"
meta_title: "Experiment Groups Selections in Polyaxon - Core Concepts"
meta_description: "An Experiment Group Selections is a way to organize and compare your experiments."
tags:
    - concepts
    - polyaxon
    - experimentation
    - experiment_groups
    - architecture
sidebar: "concepts"
---
Assuming that you have already a [project](/concepts/projects/) created and initialized,
and you uploaded your code consisting of a single file `train.py` that accepts 2 parameters

  * learning rate `lr`
  * batch size `batch_size`

If you created a large number of experiments in project, and you only wanted to compare a subset of these experiments, 
Polyaxon provides a way to create a selection, a selection, basically, allows you to group these experiments so that you can create visualizations, 
and crete a tensorboard showing only these experiments.

## Select the experiments

To create an experiment group selection, you need to select the experiments that you want to compare:

![select-experiments](../../content/images/concepts/selection/select-experiments.png)

## Create the experiments group selection

When select experiments in the table view, a new button will show to act on the selection, a couple of actions are possible:

 * Stopping all the experiments
 * Deleting all the experiments
 * Creating a selection
 * Adding the experiments to an existing selection
 

![create-selection](../../content/images/concepts/selection/create-selection.png)

![create-selection](../../content/images/concepts/selection/create-selection2.png)

We can check that the new selection was created

![create-selection](../../content/images/concepts/selection/check-selection.png)

We can see that the new group has a different type: `selection` compared to hyperparameters tuning groups `study`.

We can also use the CLI to access this group:

```bash
polyaxon group -g 4 get
```

## Compare the experiments in the selection

You can access a table view containing only the experiments selected:

![create-selection](../../content/images/concepts/selection/check-selection-experiments.png)

```bash
polyaxon group -g 4 experiments -m


Experiments for experiment group `4`.


Navigation:

-----  -
count  3
-----  -

Experiments:

  id  unique_name          total_run        loss    accuracy    precision
----  -------------------  -----------  --------  ----------  -----------
  62  root.quick-start.62  2m 18s       0.068052      0.9799     0.997565
  64  root.quick-start.64  1m 34s       0.157377      0.9521     0.998999
  63  root.quick-start.63  1m 37s       0.246496      0.9285     0.997004
```


```bash
polyaxon group -g 4 experiments -d


Experiments for experiment group `4`.


Navigation:

-----  -
count  3
-----  -

Experiments:

  id  unique_name            dropout    num_steps  activation      batch_size    num_epochs    learning_rate
----  -------------------  ---------  -----------  ------------  ------------  ------------  ---------------
  62  root.quick-start.62       0.25          500  relu                   128             1           0.001
  64  root.quick-start.64       0.5           300  relu                    64             1           0.0002
  63  root.quick-start.63       0.5           300  relu                    64             1           0.0001
```

You can compare the experiment using the native dashboard:

![create-selection](../../content/images/concepts/selection/check-selection-metrics.png)

## Creating a tensorboard to compare the experiments

```bash
polyaxon tensorboard -g 4 start
```
