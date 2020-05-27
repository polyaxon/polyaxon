---
title: "Quick Start"
sub_link: "quick-start"
meta_title: "Polyaxon quick start tutorial - Core Concepts"
meta_description: "Get started with Polyaxon and become familiar with the ecosystem of Polyaxon with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
    - tutorials
    - concepts
    - quick-start
sidebar: "core"
---

Let’s look at an example of how you can use Polyaxon for running deep learning experiments.
This example assumes that both Polyaxon is [installed](/docs/setup/) and running.

### Create a project 

You can create a project using [Polyaxon UI](/docs/management/ui/projects/) or with [Polyaxon CLI](/docs/core/cli/project/#project-create)

This example uses a [public Github repo](https://github.com/polyaxon/polyaxon-quick-start) 
for hosting the project and the polyaxonfile manifests, similar results can be achieved using local folder or other platforms, e.g. GitLab, Bitbucket, ...

## Start an experiment

Let's run a first experiment

```bash
$ polyaxon run --url=https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/experimentation/simple.yml -l
```

> For more details about this command please run `polyaxon run --help`, 
or check the [command reference](/docs/core/cli/run/)

The `-l` flag indicates that we want to stream the logs after starting the experiment.


## Start a Tensorboard 

Let's start a tensorboard to see the results:

```bash
$ polyaxon run --hub tensorboard:single-run -P uuid=UUID -w
```

![run-dashboards](../../../../content/images/dashboard/runs/dashboards-tensorboard.png)

## Let's check the results on the dashboard as well

```bash
$ polyaxon dashboard -y
```

> For more details about this command please run `polyaxon dashboard --help`, 
or check the [command reference](/docs/core/cli/dashboard/)

We can see that Polyaxon has logged some information automatically about our run:

 
![run-dashboards-many](../../../../content/images/dashboard/runs/dashboards-many.png)

Please check the [runs dashboard](/docs/management/runs-dashboard/) and the 
[visualization section](/docs/experimentation/visualizations/) for more details. 

## Congratulations 

You've trained your first experiments with Polyaxon, visualized the results in Tensorboard and tracked metrics, with two commands. 

Behind the scene a couple of things have happened:

 * You synced your GitHub project and used the last commit.
 * You ran a container with a custom image and command to train a model.
 * You persisted your logs and outputs.
 * You visualized the results using Polyaxon's native dashboard and Tensorboard.

To gain a deeper understanding of what happened and how Polyaxon can help you iterate faster with your experimentation,
please check the next section of [this tutorial](/docs/core/quick-start/components/)
