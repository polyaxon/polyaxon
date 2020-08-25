---
title: "Polyaxon Python Library"
sub_link: "python-library"
meta_title: "Polyaxon Python Library - Polyaxon References"
meta_description: "Use our Python library to instrument your machine learning model and track experiments, create Polyaxonfile specification, and extend Polyaxon's behavior. Setup should only take a few lines of code. If you're using a popular framework, we have a number of integrations to make setting up Polyaxon easy."
visibility: public
status: published
is_index: true
tags:
    - specifications
    - polyaxon
    - python
sidebar: "core"
---

Use Polyaxon Python library to create Polyaxonfile specification, to interact with Polyaxon API in a programmatic way, 
to instrument your machine learning model and track experiments, create custom visualizations, and to extend Polyaxon's behavior.

## Install

```bash
$ pip install -U polyaxon
```

N.B. `polyaxon` library is Python 3.5+ package, if you are still using Python 2 `polyaxon-sdk` is python 2/3 compatible.

## CLI

[Polyaxon CLI](/docs/core/cli/) is a tool and a client to interact with Polyaxon, it allows you to manage your cluster, projects, and experiments. 

## Clients

This module includes a client that can be used to interact with Polyaxon API in a programmatic way.


 * [Client Reference](/docs/core/python-library/polyaxon-client/): Auto-configurable and high-level base client that abstract the need to set a configuration for each service.
 * [Project Client](/docs/core/python-library/polyaxon-client/): A client to communicate with Polyaxon projects endpoints.
 * [Run Client](/docs/core/python-library/run-client/): A client to communicate with Polyaxon runs endpoints.


## Tracking Client

The [tracking client](/docs/experimentation/tracking/) is an extension and a subclass 
of the [Run Client](/docs/core/python-library/run-client/) with more methods for machine learning experiment tracking.

## Run Plot client

The [RunPlot and MultiRunPlot classes](/docs/experimentation/visualizations/) are also extensions and a subclasses 
of the [Run Client](/docs/core/python-library/run-client/) with more functionalities 
to drive visualization programmatically using [Plotly Express](https://plotly.com/python/plotly-express/) and [HiPlot](https://github.com/facebookresearch/hiplot).


## Disabling Polyaxon clients without changing the code

Since using the Polyaxon client and the tracking API requires code change, e.g.

```python
# Polyaxon experiment
experiment = Run()
# training code ...
# Metrics reporting
experiment.log_metrics(step=1000, loss=0.01, accuracy=0.97)
``` 

Users might need to run the same code outside of a Polyaxon context, 
which will break since Polyaxon related operations perform API calls.
  
Users won't need to perform any change to their code, 
they just need to set an environment variable `POLYAXON_NO_OP` to true/1, and the Polyaxon related code will be ignored.   


## Authentication

### In-cluster

All Polyaxon clients and libraries will be configured automatically if used in-cluster. 

e.g.

```python
run_client = RunClient()
```

Polyaxon provides a context for all its runs enabling users to access scoped tokens to communicate with the API.

### Locally with an authenticated Polyaxon CLI

If your Polyaxon CLI is authenticated, the Polyaxon client will be configured 
automatically with the CLI authentication information.

e.g.

```python
run_client = RunClient()
```

The client will check for the currently authenticated user and raise if non found.

### Not in-cluster and no authenticated CLI

When you need to  authenticate a client in an environment outside of a Polyaxon cluster and no authenticated CLI, Polyaxon provides several options:

#### Authentication with Environment variables:
    
You can set environment variables containing:
    
    * `POLYAXON_AUTH_TOKEN`
    * `POLYAXON_HOST`

Once these environment variables are set, you can instantiate your client, e.g.

```python
run_client = RunClient()
```

Authentication using environment variables could be useful to keep your code behave similarly in different environments.
    
#### Provide an authenticated client:

```python
client = PolyaxonClient(token=MY_TOKEN, config=ClientConfig(host=HOST, use_https=None, verify_ssl=None))
run_client = RunClient(owner="org1", project="project-name", run_uuid="uuid", client=client)
```

## Reading Polyaxonfiles

In order to use Polyaxon users have to create and execute Polyaxonfiles, these files use a
[specification](/docs/core/specification/) to describe how experiments, jobs, services should be scheduled and executed.
Users can author and read Polyaxonfiles in a programmatic way using Python. 


You can use the Python library to read and validate YAML/Json files, Python objects, or Python dictionaries:

### Python objects

```python
from polyaxon.polyflow import V1Component, V1Operation

component = V1Component(...)
operation = V1Operation(...)
```

### Known specification kind

If you know the kind of Polyaxonfile or dict, you can use directly the corresponding specification to read the content:

```python
from polyaxon.polyaxonfile import ComponentSpecification, OperationSpecification

component = ComponentSpecification.read(data)
operation = OperationSpecification.read(data)
```

### Reading a Python dictionary


```python
from polyaxon.polyaxonfile import ComponentSpecification

plx_file = ComponentSpecification.read({'version': 1, 'kind': 'component', 'run': ...})
```

### Reading multiple Python dictionaries

You can also pass several dictionaries to override a specific section

```python
from polyaxon.polyaxonfile import ComponentSpecification

plx_file = ComponentSpecification.read([group_dict, {'run': {'cmd': 'override_command'}}])
```

### Reading a single file

Sometimes you might not know the content of a file, Polyaxon provides a generic function to resolve the content of a file(s) to the correct specification kind. 

```python
from polyaxon.polyaxonfile import check_polyaxonfile

plx_file = check_polyaxonfile(polyaxonfile='path/to/polyaxonfile.yaml')
...
plx_file = check_polyaxonfile(url='https://raw.githubusercontent.com/...')
...
plx_file = check_polyaxonfile(hub='component:latest', params={"foo": "bar"})
```

### Reading multiple files

You can pass multiple files, the function will follow the order and each time update the sections based on the latest files.

```python
from polyaxon.polyaxonfile import check_polyaxonfile

plx_file = check_polyaxonfile(polyaxonfile=['path/to/polyaxonfile1.yaml', 'path/to/polyaxonfile2_to_override_values_from_file1.json'])
```

### Reading multiple files and dictionaries

You can also opt to read a file/files (YAML and Json) and only use a Python dictionary to update a specific section

```python
from polyaxon.polyaxonfile import get_specification

plx_file = get_specification(['path/to/yaml_file.yaml', 'path/to/json_file.json', {'run': {'cmd': 'override_command'}}])
```

### Using PolyaxonFiles

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

## Exceptions

Polyaxon raises several exceptions during the parsing and validation of a Polyaxonfile or configurations, all classes are derived from:

```bash
from polyaxon.exceptions import PolyaxonException
```
