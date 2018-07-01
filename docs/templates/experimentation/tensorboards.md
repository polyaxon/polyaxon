Polyaxon allows users to run tensorboard jobs on project, experiment, and experiment group level, these jobs are subject to the same permissions of the project they belong to.


[Tensorboard](https://www.tensorflow.org/programmers_guide/summaries_and_tensorboard) is a visualization tool for Tensorflow projects.
Tensorboard can help visualize the Tensorflow computation graph and plot quantitative metrics about your run.

## Start tensorboard

We assume that you have already a [project](projects) created and initialized, and code uploaded.

To start tensorboard for a project, run the following command in your terminal

```bash
$ polyaxon tensorboard start


Tensorboard is being deployed for project `mnist`

It may take some time before you can access the dashboard.

Your Tensorboard will be available on:

    http://192.168.64.6:31122/tensorboard/root/quick-start/
```

This will start tensorboard with the default options,
if you which to start tensorboard with a different Tensorflow image, or custom resources,
you need to create a polyaxonfile containing:

 * [version](/polyaxonfile_specification/sections#version)
 * [project](/polyaxonfile_specification/sections#project)
 * [run](/polyaxonfile_specification/sections#version)

For example to start tensorboard with Tensorflow 1.6, you need to define a new polyaxonfile_tensorboard.yml with the following options:


```yaml
---
version: 1

kind: tensorboard

environment:
  resources:
    cpu:
      requests: 2
      limits: 4
    memory:
      requests: 512
      limits: 2048

build:
  image: tensorflow/tensorflow:1.6.0-py3
```

You can also start a tensorboard for a specific experiment, or for aggregating metrics from all experiments in a group.


```bash
$ polyaxon tensorboard -xp 13 start


Tensorboard is being deployed for experiment 13

It may take some time before you can access the dashboard.

Your Tensorboard will be available on:

    http://192.168.64.6:31122/tensorboard/root/quick-start/experiments/13/
```


```bash
$ polyaxon tensorboard -g 3 start


Tensorboard is being deployed for experiment group 3

It may take some time before you can access the dashboard.

Your Tensorboard will be available on:

    http://192.168.64.6:31122/tensorboard/root/quick-start/groups/13/
```


### Stop tensorboard

To stop tensorboard, run the following command in your terminal

For project tensorboard

```bash
$ polyaxon tensorboard stop
```

For experiment tensorboard

```bash
$ polyaxon tensorboard -xp 13 stop
```

For experiment group tensorboard

```bash
$ polyaxon tensorboard -f 3 stop
```

!!! info "More details"
    For more details about this command please run `polyaxon tensorboard --help`,
    or check the [command reference](/polyaxon_cli/commands/tensorboard)
