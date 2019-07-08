---
title: "Polyaxonfile Python Specification"
sub_link: "polyaxonfile-python-specification"
meta_title: "Polyaxonfile Python Specification - Polyaxon References"
meta_description: "In order to use Polyaxon, users need to create YAML/Json polyaxonfiles or they author these specs programatically. These files use a specification to describe how experiments, experiment groups, jobs, plugins should run on Polyaxon."
visibility: public
status: published
tags:
    - specifications
    - polyaxon
    - python
---

In order to use Polyaxon, users can author and read polyaxonfiles in programmatic way using Python. 
These files use a [specification](/references/polyaxonfile-yaml-specification/) to describe how experiments, experiment groups, jobs, plugins should run on Polyaxon.

## Reading Polyaxonfiles

You can use the `PolyaxonFile` object to read and validate YAML/Json files or Python dictionaries: 

### Reading a single file

```python
from polyaxon_schemas.polyaxonfile import PolyaxonFile

plx_file = PolyaxonFile('path/to/polyaxonfile.yaml')
plx_file.specification   # This is the config and has access to all section as python objects
```

### Reading a multiple files

You can pass multiple files, `PolyaxonFile` will follow the order and each time update the sections based on the latest files.

```python
from polyaxon_schemas.polyaxonfile import PolyaxonFile

plx_file = PolyaxonFile(['path/to/polyaxonfile1.yaml', 'path/to/polyaxonfile2_to_override_values_from_file1.json'])
```

### Reading a Python dictionary

Similar to reading files, you can read dictionaries as well.

```python
from polyaxon_schemas.polyaxonfile import PolyaxonFile

plx_file = PolyaxonFile({'version': 1, 'kind': 'group', 'hptuning': ...})
```

### Reading multiple Python dictionaries

You can also pass several dictionaries to override a specific section

```python
from polyaxon_schemas.polyaxonfile import PolyaxonFile

plx_file = PolyaxonFile([group_dict, {'run': {'cmd': 'override_command'}}])
```

### Reading multiple files and Python dictionaries

You can also opt to read a file/files (YAML and Json) and only use a Python dictionary to update a specific section

```python
from polyaxon_schemas.polyaxonfile import PolyaxonFile

plx_file = PolyaxonFile(['path/to/yaml_file.yaml', 'path/to/json_file.json', {'run': {'cmd': 'override_command'}}])
```

## Using PolyaxonFile

The `PolyaxonFile` class is generic and can read any polyaxonfile primitive, i.e. `experiment`, `group`, `job`, `build` .... If the file passed is valid, 
you will be able to get the specification and the kind, for example, let's consider this simple polyaxonfile:

```yaml
version: 1

kind: experiment

tags: ['foo', 'bar']

params:
  num_masks: 2

build:
  image: my_image
  build_steps:
    - pip install package1
  env_vars:
    - ['KEY1', 'en_US.UTF-8']
    - ['KEY2', 2]

run:
  cmd: video_prediction_train --num_masks={{num_masks}}
```

You can read this file:

```python
from polyaxon_schemas.polyaxonfile import PolyaxonFile
from polyaxon_schemas.specs import ExperimentSpecification

plx_file = PolyaxonFile('path/to/polyaxonfile.yaml')

assert plx_file.is_experiment == True
assert isinstance(plx_file.specification, ExperimentSpecification)

spec = plx_file.specification
# In order to resolve the spec we need to call apply context
# Context is any dependency or references that need to be resolved for validating the specification
spec.apply_context()

assert spec.version == 1
assert spec.logging is None
assert sorted(spec.tags) == sorted(['foo', 'bar'])
assert sorted(spec.params) == {'num_masks': 2}

assert spec.build.image == 'my_image'
assert spec.build.build_steps == ['pip install package1']
assert spec.build.env_vars == [['KEY1', 'en_US.UTF-8'], ['KEY2', 2]]
# You can also get the build section as dict for instance
spec.build.to_dict()

assert spec.run.cmd == 'video_prediction_train --num_masks=2'
```  

## Specifications

You can also use the specification directly to read a file/dictionary:

```python
from polyaxon_schemas.specs.build import BuildSpecification
from polyaxon_schemas.specs.experiment import ExperimentSpecification
from polyaxon_schemas.specs.group import GroupSpecification
from polyaxon_schemas.specs.job import JobSpecification
from polyaxon_schemas.specs.notebook import NotebookSpecification
from polyaxon_schemas.specs.tensorboard import TensorboardSpecification
```


## Exceptions

Polyaxon raises several exception during the parsing and validation of Polyaxonfile or configurations:

```bash
from polyaxon_schemas.exceptions import PolyaxonfileError, PolyaxonfileError, PolyaxonSchemaError
```
