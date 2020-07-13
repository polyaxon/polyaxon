---
title: "Productive iterations with templates"
title_link: "Productive iterations with templates"
meta_title: "Productive iterations with templates - Guide"
meta_description: "Developing machine learning models requires several iterations, Polyaxon users can create several templates to run faster iterations."
custom_excerpt: "Developing machine learning models requires several iterations, Polyaxon users can create several templates to easily update the node scheduling or parameters."
featured: true
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
    - guides
    - experimentation
---

Developing machine learning models requires several iterations, some of these iteration require:
 * changing the parameters
 * running the experiments on GPU nodes
 * running the experiments in distributed ways

The following sections will give a high-level examples of how to create several templates to either update the parameters or the node used for running your experiments. 
Similar approach can be used to override polyaxonfiles used for jobs, notebooks, tensorboards, ... 

## Standard and simple polyaxonfiles

The best way to rapidly develop experiments, we recommend creating a standard polyaxonfile with your main command and parameters:

```yaml
version: 1

kind: experiment

params:
  lr: 0.01
  batch_size: 128

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install -r polyaxon_requirements.txt

run:
  cmd: python3 train.py --batch-size={{ batch_size }} --lr={{ lr }}
```

And running this file:

```bash
polyaxon run -f polyaxonfile.yaml
```

## Overriding the parameters

```yaml
version: 1

kind: experiment

params:
  lr: 0.2
  batch_size: 64
```

Using this override file:

```bash
polyaxon run -f polyaxonfile.yaml -f polyaxonfile_params.yaml
```

By running this command your experiment will be started using the params of the override file.

## Overriding the node scheduling


```yaml
version: 1

kind: experiment

environment:
  node_selector:
    node_label: node_value
  
  resources:
    cpu:
      requests: 2
      limits: 4
    gpu:
      requests: 1
      limits: 1
    memory:
      requests: 512
      limits: 2048
```

Using this override file:

```bash
polyaxon run -f polyaxonfile.yaml -f polyaxonfile_node_scheduling.yaml
```

By running this command your experiment will use the node selector and request the resources in the environment section.
