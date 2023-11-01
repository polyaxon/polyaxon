---
title: "Reading Polyaxonfiles"
sub_link: "python-library/reading-polyaxonfiles"
meta_title: "Reading polyaxonfile using the Python interface - Python Client References"
meta_description: "Polyaxon's Python library allows to turn off all API calls and silently pass through all function calls."
visibility: public
status: published
tags:
  - specifications
  - client
  - api
  - polyaxon
  - python
sidebar: "core"
---

## Overview

Polyaxon users have to create and execute Polyaxonfiles, these files use a
[specification](/docs/core/specification/) to describe how experiments, jobs, services should be scheduled and executed.
Users can author and read Polyaxonfiles in a programmatic way using Python.


You can use the Python library to read and validate YAML/Json files, Python objects, or Python dictionaries:

## Python objects

```python
from polyaxon.schemas import V1Component, V1Operation

component = V1Component(...)
operation = V1Operation(...)
```

## Known specification kind

If you know the kind of Polyaxonfile or dict, you can use directly the corresponding specification to read the content:

```python
from polyaxon.polyaxonfile import ComponentSpecification, OperationSpecification

component = ComponentSpecification.read(data)
operation = OperationSpecification.read(data)
```

## Reading a Python dictionary

```python
from polyaxon.polyaxonfile import ComponentSpecification

plx_file = ComponentSpecification.read({'version': 1, 'kind': 'component', 'run': ...})
```

## Reading multiple Python dictionaries

You can also pass several dictionaries to override a specific section

```python
from polyaxon.polyaxonfile import ComponentSpecification

plx_file = ComponentSpecification.read([group_dict, {'run': {'cmd': 'override_command'}}])
```

## Reading a single file

Sometimes you might not know the content of a file, Polyaxon provides a generic function to resolve the content of a file(s) to the correct specification kind.

```python
from polyaxon.polyaxonfile import check_polyaxonfile

plx_file = check_polyaxonfile(polyaxonfile='path/to/polyaxonfile.yaml')
...
plx_file = check_polyaxonfile(url='https://raw.githubusercontent.com/...')
...
plx_file = check_polyaxonfile(hub='component:latest', params={"foo": "bar"})
```

## Reading multiple files

You can pass multiple files, the function will follow the order and each time update the sections based on the latest files.

```python
from polyaxon.polyaxonfile import check_polyaxonfile

plx_file = check_polyaxonfile(polyaxonfile=['path/to/polyaxonfile1.yaml',
                                            'path/to/polyaxonfile2_to_override_values_from_file1.json'])
```

## Reading multiple files and dictionaries

You can also opt to read a file/files (YAML and Json) and only use a Python dictionary to update a specific section

```python
from polyaxon.polyaxonfile import get_specification

plx_file = get_specification(
    ['path/to/yaml_file.yaml', 'path/to/json_file.json', {'run': {'cmd': 'override_command'}}])
```

## Using PolyaxonFiles

Once you read the content of Polyaxonfile, you will get a Python class if the file passed and is valid,
and you will be able to interact with it as any Python object.

```yaml
version: 1
kind: operation
name: test
tags: ['foo', 'bar']
params:
  num_masks: {value: 2}

component:
  run:
    kind: job
    container:
      image: some-image:version
      command: some-command
```

You can read this file:

```python
assert spec.name == "test"
component = spec.component
assert isinstance(component.run.container, V1Container)
assert component.run.container.image == "some-image:version"
assert component.run.container.command == "some-command"
```

Please check the [specification docs](/docs/core/specification/)
