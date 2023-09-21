---
title: "Passing params with the Python library"
sub_link: "passing-params/with-python-library"
meta_title: "Passing params with the python library - Core Concepts"
meta_description: "Sometimes you may need to handle or request the parameters directly from the API or using the Python library."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

Sometimes you may need to handle or request the resolved inputs and outputs directly from the API or using the Python library.

## Overview

Polyaxon provides a [Python Library](/docs/core/python-library/polyaxon-client/) that exposes several methods to fetch information about a run or the currently running operation.

Users can use the library to request the full resolved params (inputs and outputs) and use it during the runtime of their programs. They can additionally add, update,
or reset the inputs or outputs programmatically.

## Example with the `RunClient`

Let's look at a simple program that just prints some information based on an input using the basic [Runclient](/docs/core/python-library/run-client/):

```python
from polyaxon.client import RunClient

client = RunClient()
client.refresh_data()
print(client.get_inputs())
```

In order to run this program, we can use the following polyaxonfile `echo.yaml`:


```yaml
version: 1.1
kind: component
inputs:
- name: message
  type: str
  isOptional: true
  value: "Default message"
run:
  kind: job
  init:
    - file:
        content: |
          from polyaxon.client import RunClient

          client = RunClient()
          client.refresh_data()
          print(client.get_inputs())

        filename: echo.py
  container:
    image: polyaxon/polyaxon-quick-start
    workingDir: "{{ globals.artifacts_path }}"
    command: [python3, -u, echo.py]
```

Now you can run multiple version of this example:

```bash
polyaxon run -f echo.yaml -P message="test 1" -l
```

```bash
polyaxon run -f echo.yaml -P message="test 2" -l
```

## Example with the tracking module

In the previous example we used the `RunClient` which is a high-level Python library to interact with the Run API.
You probably noticed that we had to refresh the data manually using `client.refresh_data()`.

In most situations, and especially for operations running in-cluster, users will need to interact with their runs using the [run tracking class](/docs/experimentation/tracking/client/) or the [tracking module](/docs/experimentation/tracking/module/),
which provides several more methods for logging and versioning results.

The module also performs several more initializations steps, including an implicit refresh, to provide the latest version of the metadata before your program starts.

Let's rewrite the program:

```python
from polyaxon import tracking

tracking.init()
print(tracking.TRACKING_RUN.get_inputs())
```

Let's update the component:


```yaml
version: 1.1
kind: component
inputs:
- name: message
  type: str
  isOptional: true
  value: "Default message"
run:
  kind: job
  init:
    - file:
        content: |
          from polyaxon import tracking

          tracking.init()
          print(tracking.TRACKING_RUN.get_inputs())

        filename: echo.py
  container:
    image: polyaxon/polyaxon-quick-start
    workingDir: "{{ globals.artifacts_path }}"
    command: [python3, -u, echo.py]
```

Now you can run multiple version of this example:

```bash
polyaxon run -f echo.yaml -P message="test 1" -l
```

```bash
polyaxon run -f echo.yaml -P message="test 2" -l
```
