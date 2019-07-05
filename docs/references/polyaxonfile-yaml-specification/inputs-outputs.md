---
title: "Inputs/Outputs - Polyaxonfile YAML Specification"
sub_link: "polyaxonfile-yaml-specification/inputs-outputs"
meta_title: "Inputs/Outputs Section - Polyaxonfile YAML Specification Sections - Polyaxon References"
meta_description: "Inputs/Outputs Section - Polyaxonfile YAML Specification Sections."
visibility: public
status: published
tags:
    - specifications
    - polyaxon
    - yaml
sidebar: "polyaxon-yaml-specification"
---

## Overview

Starting from v0.5, Polyaxon specification introduced 2 new sections that allow to operationalize you experiments/jobs/builds.


An input/output section includes a name, a description, an optional type to check the value passed, a flag to tell if the input/output is optional, and a default value if it is optional.

 * name `required`: the name of this input/output, the name must be a slug.
 * description: an optional description of this input/output, giving a description will self-document the component for future use, and will be used by the UI.
 * type: the type of this input/output, if given any value that is passed to will be checked for validation, 
    in case the component is used in a pipeline, the Polyaxon will validate chaining from one operation to another will before any execution.
    * Possible types: `int`, `float`, `str`, `bool`, `dict`, `uri`, `auth`, `list`, `gcs_path`, `s3_path`, `azure_path`, `path`, `metric`, `metadata`
 * default: a default value to use in case no params is passed.
 * is_optional: by default inputs are required, and outputs will be validate post-run to check that outputs meet the specs.  
 * is_list: a flag to check if the input should be a list of `type`.
 * is_flag: this can be used with `type == bool` and it will turn resolve the param as flag or remove it `--name`
 * options: to validate the values passed to the input against this list of options.
 

## Example turning an experiment with params to a typed experiment

Let's take this experiment with some params:

```yaml
version: 1

kind: experiment

declarations:
  batch_size: 128
  num_steps: 500
  learning_rate: 0.001
  dropout: 0.25
  num_epochs: 1
  activation: relu

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip3 install --no-cache-dir -U polyaxon-client==0.5.0

run:
  cmd:  python3 model.py --batch_size={{ batch_size }} \
                         --num_steps={{ num_steps }} \
                         --learning_rate={{ learning_rate }} \
                         --dropout={{ dropout }} \
                         --num_epochs={{ num_epochs }} \
                         --activation={{ activation }}

```

We can declare this same experiment with inputs:

```yaml
version: 1

kind: experiment

inputs:
  - name: batch_size
    description: batch size
    is_optional: true
    default: 128
    type: int
  - name: num_steps
    is_optional: true
    default: 500
    type: int
  - name: learning_rate
    is_optional: true
    default: 0.001
    type: float
  - name: dropout
    is_optional: true
    default: 0.25
    type: float
  - name: num_epochs
    is_optional: true
    default: 1
    type: int
  - name: activation
    is_optional: true
    default: relu
    type: str

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip3 install --no-cache-dir -U polyaxon-client==0.5.0

run:
  cmd:  python3 model.py --batch_size={{ batch_size }} \
                         --num_steps={{ num_steps }} \
                         --learning_rate={{ learning_rate }} \
                         --dropout={{ dropout }} \
                         --num_epochs={{ num_epochs }} \
                         --activation={{ activation }}
```

## Running a typed experiment

Using the Polyaxon cli we can now run this experiment and override the inputs' default values:

```bash
polyaxon run -f polyaxonfile.yaml -P activation=sigmoid -P dropout=0.4

``` 

this will result in an experiment where a param is passed and validate against the input to check that value correspond to the type of the input.

## Required inputs

if we decide for instance to make the activation required:

````yaml
....

inputs:
  ...
  - name: activation
    type: str
  ...
...
````

By changing this input, polyaxon can not run this experiment, because it requires that the user passes a param activation:


```bash
polyaxon run -f polyaxonfile.yaml -P activation=sigmoid
```

If this experiment is used as one of the templates of a pipelines, the spec will check that any operation using 
this template receives a valid param for activation before attempting to run it, and discover that one of operations fail later.
