---
title: "Iterate programmatically"
sub_link: "iterative-process/iterate-programmatically"
meta_title: "Programmatic Iteration with the python client - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Programmatic Iteration with the python client - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - client
  - quick-start
sidebar: "intro"
---

We briefly went through one aspect of the programmatic experience in the guide [iterate-in-notebooks](/docs/intro/iterative-process/iterate-in-notebooks/).

In this sections we will learn how to drive the complete workflow, i.e. creating valid manifests (Polyaxonfiles) and performing API calls using the Python client.

In this guide we will recreate the manifests that we used before using Polyaxon's Python library.

## Creating components in Python

Let's look again at the typed component that we used for running the experiments:

```yaml
version: 1.1
kind: component
name: typed-experiment
description: experiment with inputs
tags: [examples]

inputs:
- {name: conv1_size, type: int, value: 32, isOptional: true}
- {name: conv2_size, type: int, value: 64, isOptional: true}
- {name: dropout, type: float, value: 0.2, isOptional: true}
- {name: hidden1_size, type: int, value: 500, isOptional: true}
- {name: conv_activation, type: str, value: relu, isOptional: true}
- {name: dense_activation, type: str, value: relu, isOptional: true}
- {name: optimizer, type: str, value: adam, isOptional: true}
- {name: learning_rate, type: float, value: 0.01, isOptional: true}
- {name: epochs, type: int}
outputs:
- {name: loss, type: float}
- {name: accuracy, type: float}

run:
  kind: job
  init:
  - git: {url: "https://github.com/polyaxon/polyaxon-quick-start"}
  container:
    image: polyaxon/polyaxon-quick-start
    command: [python3, "{{ globals.artifacts_path }} + /polyaxon-quick-start/model.py"]
    args: [
      "--conv1_size={{ conv1_size }}",
      "--conv2_size={{ conv2_size }}",
      "--dropout={{ dropout }}",
      "--hidden1_size={{ hidden1_size }}",
      "--optimizer={{ optimizer }}",
      "--conv_activation={{ conv_activation }}",
      "--dense_activation={{ dense_activation }}",
      "--learning_rate={{ learning_rate }}",
      "--epochs={{ epochs }}"
    ]
```

This component does not use all sections that Polyaxon exposes, but similar logic should be used to include additional sections.

```python
from polyaxon import types
from polyaxon.k8s import V1Container
from polyaxon.schemas import V1GitType
from polyaxon.schemas import V1Component, V1Init, V1IO, V1Job

inputs = [
    V1IO(name="conv1_size", type=types.INT, value=32, is_optional=True),
    V1IO(name="conv2_size", type=types.INT, value=64, is_optional=True),
    V1IO(name="dropout", type=types.FLOAT, value=0.2, is_optional=True),
    V1IO(name="hidden1_size", type=types.INT, value=500, is_optional=True),
    V1IO(name="conv_activation", type=types.STR, value="relu", is_optional=True),
    V1IO(name="dense_activation", type=types.STR, value="relu", is_optional=True),
    V1IO(name="optimizer", type=types.STR, value="adam", is_optional=True),
    V1IO(name="learning_rate", type=types.FLOAT, value=0.01, is_optional=True),
    V1IO(name="epochs", type=types.INT),
]

outputs = [
    V1IO(name="loss", type=types.FLOAT),
    V1IO(name="accuracy", type=types.FLOAT),
]

job = V1Job(
    init=[V1Init(git=V1GitType(url="https://github.com/polyaxon/polyaxon-quick-start"))],
    container=V1Container(
        image="polyaxon/polyaxon-quick-start",
        working_dir="{{ globals.artifacts_path }}",
        command=["python3", "polyaxon-quick-start/model.py"],
        args=[
            "--conv1_size={{ conv1_size }}",
            "--conv2_size={{ conv2_size }}",
            "--dropout={{ dropout }}",
            "--hidden1_size={{ hidden1_size }}",
            "--optimizer={{ optimizer }}",
            "--conv_activation={{ conv_activation }}",
            "--dense_activation={{ dense_activation }}",
            "--learning_rate={{ learning_rate }}",
            "--epochs={{ epochs }}"
        ]
    ),
)

component = V1Component(
    name="typed-experiment",
    description="experiment with inputs",
    tags=["examples"],
    inputs=inputs,
    outputs=outputs,
    run=job,
)
```

It's also possible to create a component and then assign the IO or the run fields after:

```python
from polyaxon.schemas import V1Cache, V1Component, V1Job

...
component = V1Component()
component.run = V1Job(...)
component.queue = "agent/queue"
component.cache = V1Cache(...)
...
```

## Running the python manifests programmatically

In order to execute the previous component programmatically, we will use `RunClient.create` method:

```python
from polyaxon.client import RunClient
from polyaxon.schemas import V1Operation, V1Param

client = RunClient(...)

operation = V1Operation(
    component=component,
    params={
        "optimizer": V1Param(value="sgd"),
        "epochs": V1Param(value=1),
    },
)

client.create(content=operation)
```

Since the component has one input that is not optional, we should pass at least one param `"epochs": V1Param(value=1)`.

It's possible to pass additional override information with the operation:

```python
from polyaxon.client import RunClient
from polyaxon.schemas import V1Environment, V1Operation, V1Param, V1Job

client = RunClient(...)

operation = V1Operation(
    name="new-name",
    description="new-desc",
    tags=["new-tag"],
    component=component,
    params={
        "epochs": V1Param(value=1),
        "optimizer": V1Param(value="sgd"),
        "learning_rate": V1Param(value=0.001),
    },
    run_patch=V1Job(environment=V1Environment(labels={"key": "value"}))
)

client.create(content=operation)
```

If you are running on Polyaxon EE or Polyaxon Cloud, you can also pass a matrix definition:

```python
from polyaxon.client import RunClient
from polyaxon.schemas import (
    V1Environment,
    V1Operation,
    V1Param,
    V1Job,
    V1RandomSearch,
    V1HpChoice,
    V1HpLinSpace,
)

client = RunClient(...)

operation = V1Operation(
    name="new-name",
    description="new-desc",
    tags=["new-tag"],
    component=component,
    params={
        "epochs": V1Param(value=1),
        "optimizer": V1Param(value="sgd"),
        "learning_rate": V1Param(value=0.001),
    },
    run_patch=V1Job(environment=V1Environment(labels={"key": "value"})),
    matrix=V1RandomSearch(
        num_runs=10,
        params={
            "learning_rate": V1HpLinSpace(value="0.001:0.1:5"),
            "dropout": V1HpChoice(value=[0.25, 0.3]),
            "conv_activation": V1HpChoice(value=[[relu, 0.1], [sigmoid, 0.8]]),
            "epochs": V1HpChoice(value=[5, 10]),
        }
    )
)

client.create(content=operation)
```

## Running the python manifests with the CLI

By using `V1Component` and `V1Operation` it's possible to extend Polyaxon beyond the interfaces exposed via the CLI, hence allowing users to create custom workflows.

Another case for defining the component with Python, other than the programmatic execution, is to introduce testing.

Polyaxon CLI can also start new executions based on Python files similar to the YAML files. If we save the component definition in a python file `path/to/typed_experiment.py`.

We can start a new experiment by running the following command:

```bash
polyaxon run -pm path/to/typed_experiment.py:component -P epochs=10 -l
```

You probably noticed that we passed the name of the variable `component` in `typed_experiment.py:component`.
This is how we tell the CLI to execute that component by providing a variable name, by default the CLI looks for a component named `main` otherwise it raises an error.
So we need to pass a name to point to a specific variable, which is also useful if the Python module has more than one component.

For instance, if we have a Python file with 3 components:

```python
from polyaxon.schemas import V1Component

component1 = V1Component(...)
component2 = V1Component(...)
main = V1Component(...)
```

By running the following command:

```bash
polyaxon run -pm path/to/typed_experiment.py -P epochs=10 -l
```

Polyaxon will run the component named `main` by default. In order to run `component1` or `component2` we need to execute the following commands:

```bash
# component1
polyaxon run -pm path/to/typed_experiment.py:component1 -P ...

# component2
polyaxon run -pm path/to/typed_experiment.py:component2 -P ...
```

