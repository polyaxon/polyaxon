---
title: "Polyflow: Templates"
sub_link: "polyflow"
meta_title: "Polyaxon Polyflow: Templates - Polyaxon References"
meta_description: "To operationalize an experiment, a job, a build, a notebook, or a tensorboard, you can take advantage of templates."
visibility: public
status: published
tags:
    - reference
    - polyaxon
    - polyflow
    - pipelines
    - dags
    - experimentation
sidebar: "polyflow"
---

> Polyflow is in beta, please reach out to us if you want to have early access

Templates are typed Polyaxonfiles where every parameter passed should be checked against an input/output.

Templates require access to the current project to use a version of the code.

> The difference between a Template and an Action or an Event, is that Action and Event are self contained components, 
i.e. they are built and packaged independently of the project they are used in.

## Specification

A template is any [polyaxonfile primitive](/references/polyaxonfile-yaml-specification/) that declares a name, inputs and outputs needed.

 * [version](/references/polyaxonfile-yaml-specification/version/) `required`: defines the version of the file to be parsed and validated.
 * [kind](/references/polyaxonfile-yaml-specification/kind/) `required`: defines the kind of operation to run: experiment.
 * [logging](/references/polyaxonfile-yaml-specification/logging/): defines the logging.
 * name `required`: the name of the template, will be used to generate operations
 * description: a description of this template
 * [inputs](/references/polyaxonfile-yaml-specification/inputs_outputs/): the inputs of this template
 * [outputs](/references/polyaxonfile-yaml-specification/inputs_outputs/): the onputs of this template
 
 
## Example

```yaml
---
version: 1

kind: experiment

name: classifier

description: A machine learning classifier 

framework: tensorflow

inputs:
  - {name: num_steps, type: int}
  - {name: learning_rate, type: float}
  - {name: batch_size, type: int, is_optional: true, default: 128}

outputs:
  - {name: model, type: path}
  - {name: loss, type: metric}

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip3 install --no-cache-dir -U polyaxon-client==0.5.5

run:
  cmd:  python3 model.py --batch_size={{ batch_size }} \
                         --num_steps={{ num_steps }} \
                         --learning_rate={{ learning_rate }}

```
