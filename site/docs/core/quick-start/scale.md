---
title: "Quick Start: Scale"
sub_link: "quick-start/scale"
meta_title: "Scaling - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Scaling - Get started with Polyaxon and become familiar with the ecosystem of Polyaxon with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
    - tutorials
    - concepts
    - quick-start
sidebar: "core"
---

Polyaxon provides several features for scaling and automating your process.

There are different ways to scale your operations:
 * Running distributed jobs
 * Running hyperparameter tuning and parallel jobs
 * Automating a large and a complex process

Oftentimes you may want to create many experiments with different parameters and automatically manage their execution.

Polyaxon has APIs and clients that you can use with your favorite scheduler. 
It also comes with built-in support for distributed jobs, parallel executions, and an optimization and a flow engine.    

## Scaling with distributed jobs

Running a distributed job is similar to running a normal job, Polyaxon offers different [distributed runtimes](/docs/experimentation/distributed/).

In this example, we will just show a tensorflow distributed experiment based on TFJob. But the same principle applies to other supported operators. 

```yaml
version: 1.1
kind: component
run:
  kind: tfjob
  chief:
    connections: [my-training-dataset]
    container:
      image: image-with-default-entrypoint
  worker:
    replicas: 2
    environment:
      restartPolicy: OnFailure
    connections: [my-training-dataset]
    container:
      image: image-with-default-entrypoint
      resources:
        limits:
          nvidia.com/gpu: 1
```

This will start a TFJob with 1 replica of type chief and 2 workers.

## Scaling with Hyperparameter tuning 

Let's run another polyaxonfile `polyaxonfile_hyperparams.yaml`, which contains a hyperparameter tuning definition, this is the content of the file:

```yaml
version: 1.1
kind: operation
matrix:
  kind: grid
  concurrency: 2
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
urlRef: https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/experimentation/typed.yml
```

This is an operation based on the same component.
Instead of defining a single set of params, similar to what we did in previous sections of this tutorial,
this file defines a matrix, in this case, a matrix with the grid search algorithm.
It uses the same component and Polyaxon validate the space search generated against
the inputs and outputs defined in the component to validate the params.
Polyaxon will generate multiple operations based on the search space, and it will manage their execution using a pipeline.

Polyaxon provides several generators for defining a [search space](/docs/automation/optimization-engine/params/) and several 
[search algorithms for hyperparameter tuning](/docs/automation/optimization-engine/). 
There are also tools to [control the caching](/docs/automation/helpers/cache/) for experiments with similar details, 
and [concurrency](/docs/automation/helpers/concurrency/) for managing the number of parallel jobs.

Every pipeline in Polyaxon can also define [early stopping strategies](/docs/automation/helpers/early-stopping/). 

Starting a hyperparameter tuning is similar to any other operation: 

```bash
$ polyaxon run --url https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/automation/hyperparams_grid.yml
```

> For more details about this command please run `polyaxon run --help`, 
or check the [command reference](/docs/core/cli/run/)

The repo contains more hyperparameter tuning examples in the automation folder.

## Automation with DAGs

DAGs are one of the runtimes supported by Polyaxon.

The file `dag.yml` contains a DAG definition, it automates the journey we built manually in this tutorial:

```yaml
version: 1.1
kind: component
name: automated-process
description: runs an experiment, if the loss is higher than max_loss start a hyperparameter tuning process, and then print the best models
inputs:
- {name: max_loss, type: float, value: 0.01, isOptional: true, description: "max loss to start a tuning job."}
- {name: top, type: int, value: 5, isOptional: true, description: "top jobs."}
run:
  kind: dag
  operations:
  - name: build
    params:
      destination:
        value:
          name: polyaxon/polyaxon-quick-start
          connection: docker-connection
    runPatch:
      init:
      - dockerfile:
          image: "tensorflow/tensorflow:2.0.1-py3"
          run:
          - 'pip3 install --no-cache-dir -U polyaxon["polyboard","polytune"]'
          langEnv: 'en_US.UTF-8'
  - name: experiment
      urlRef: https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/experimentation/typed.yml
      dependencies: [build]
      params:
        learning_rate : 0.005
        epochs: 10
  - name: tune
    urlRef: https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/experimentation/typed.yml
    params:
      upstream_loss:
        ref: ops.experiment
        value: outputs.loss
        contextOnly: true
    condition: "{{ upstream_loss > dag.inputs.max_loss }}"
    matrix:
      kind: random
      concurrency: 2
      numRuns: 20
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
  - name: best_model
    dependencies: [experiment, tune]
    trigger: all_done
    component:
      run:
        kind: job
        init:
        - git: {url: "https://github.com/polyaxon/polyaxon-quick-start"}
        container:
          image: polyaxon/polyaxon-quick-start
          command: [python3, "{{ globals.artifacts_path }} + /polyaxon-quick-start/best_models.py"]
          args: ["--project={{ globals.project_name }}", "--top={{ dag.inputs.top }}"]
```

This DAG will start an experiment, if the experiment has a `loss > max_loss` 
it will start a tuning job based on a random search algorithm, 
finally, it will run a container to print the best 5 models.

The DAG itself is parameterized, we can pass different values for `max_loss` and `top`.

```bash
$ polyaxon run --url https://raw.githubusercontent.com/polyaxon/polyaxon-quick-start/master/automation/dag.yml -P loss=0.002 -P top=10
```

A DAG definition is also managed internally by a pipeline, which means you can also leverage all 
the pipeline tools to [control the caching](/docs/automation/helpers/cache/) for runs with similar details, 
 [concurrency](/docs/automation/helpers/concurrency/) for managing the number of parallel jobs, and [early stopping strategies](/docs/automation/helpers/early-stopping/).

To learn more about [DAGs](/docs/automation/flow-engine/).

## Learn More

You can check the [automation section](/docs/automation/) for more details about all the automation features.
