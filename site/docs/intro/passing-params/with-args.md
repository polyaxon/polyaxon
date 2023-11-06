---
title: "Passing params with args"
sub_link: "passing-params/with-args"
meta_title: "Passing parameters to your programs as args - Core Concepts"
meta_description: "Passing the parameters as args requires that you create and expose your programs as simple command-line applications."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

Passing the parameters as args requires that you create and expose your programs as simple command-line applications.

Creating command-line applications is a powerful way of exposing work, it forces users to think about how to structure and organize programs,
it provides documentation for the expected inputs and performs checks that other users can benefit from when interacting with a program.

## Passing params to a simple program

Your program can be written in any language, the only requirements to use this method for passing configurations (inputs/outputs), is that you need to provide an interface to consume arguments.

Let's consider the `echo` command, you can past this content directly to Polyaxon UI or you can save it under `echo.yaml`:

```yaml
version: 1.1
kind: component
run:
  kind: job
  container:
    image: busybox:stable
    command: ["echo", "This is a test"]
```

This is a simple program that prints information, you can run it using Polyaxon CLI:

```bash
polyaxon run -f echo.yaml -l
```

In order to run this program with multiple values, we can keep changing the message manually or we can expose the message to print as an input and pass it as an argument:

```yaml
version: 1.1
kind: component
inputs:
- name: message
  type: str
run:
  kind: job
  container:
    image: busybox:stable
    command: ["echo", "{{ message }}"]
```

Now you can run multiple version of this example without changing the polyaxonfile:

```bash
polyaxon run -f echo.yaml -P message="test 1" -l
```

```bash
polyaxon run -f echo.yaml -P message="test 2" -l
```


You can also notice that Polyaxon will track the input and will show it in the UI and the CLI:

```bash
polyaxon ops get -uid UUID

Run inputs:

-------  ------
message  test 1
-------  ------

....
```

## Multirun

Sometimes users might need to run the same job and pass different params, one way to do that is by invoking the CLI multiple times,
another way is to use `-HP`(`--hparams`) instead of `-P`(`--params`).

To pass `test 1` and `test 2` to our program without invoking the CLI multiple times:

```bash
polyaxon run -f echo.yaml -HP message='choice:["test 1","test 2"]'
```

This command will automatically create a [grid search](/docs/intro/scaling/hyperparameter-tuning/#grid-search) with the following matrix configuration:

```yaml
matrix:
  kind: grid
  params:
    message:
      kind: choice
      value:
        - test 1
        - test 2
  concurrency: 1
```

You should notice that the CLI uses the following format: `kind:value` to pass [hyperparameters](/docs/automation/optimization-engine/params/), in this case it passes the `choice` kind.
Another important aspect to notice is that matrix is of kind [grid search](/docs/automation/optimization-engine/grid-search/) and it runs the operations sequentially by setting the `concurrency` to `1`.
You can configure those options via CLI as well by passing the following extra arguments `--matrix-kind`, `--matrix-concurrency`, and `--matrix-num-runs`.

The CLI arg `-HP` is a nice way to avoid creating configuration files when iterating, however if you are to create a complex operation with multiple inputs/outputs and complex matrix defintion,
we suggest that you use a proper Polyaxonfile.
See the intro for the hyperparameter tuning in this [section](/docs/intro/scaling/hyperparameter-tuning/) and the [optimization engine reference](/docs/automation/optimization-engine/).

## Creating a custom program

Since most Polyaxon's users are data-scientists or machine learning engineers, they generally write their programs in Python, so the content of these tutorials will be in Python as well.

This is a simple application that prints your inputs, in this example we will use the `argparse` package to consume the parameters,
but the same logic can be used with [python-fire](https://github.com/google/python-fire), [click](https://github.com/pallets/click), or any other library of your choice.

```python
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--message',
        type=str,
        default="Default message")

    args = parser.parse_args()

    print(args.message)
```

We can adjust our previous polyaxonfile to run this python program, in order to avoid [uploading code](/docs/intro/iterative-process/iterate-in-notebooks/) or [cloning a repo](/docs/intro/iterative-process/iterate-with-cli-git-code/),
we will pass the python code [inline](/docs/intro/iterative-process/iterate-with-inline-scripts/):

Let's save this changes under `echo.yaml`:

```yaml
version: 1.1
kind: component
inputs:
- name: message
  type: str
run:
  kind: job
  init:
    - file:
        content: |
          import argparse

          if __name__ == '__main__':
              parser = argparse.ArgumentParser()

              parser.add_argument(
                  '--message',
                  type=str,
                  default="Default message")

              args = parser.parse_args()

              print(args.message)

        filename: echo.py
  container:
    image: polyaxon/polyaxon-quick-start
    workingDir: "{{ globals.artifacts_path }}"
    command: [python3, -u, echo.py]
    args: ["{{ params.message.as_arg }}"]
```

To run this example:

```bash
polyaxon run -f echo.yaml -P message="test 1" -l
```

## Explaining as_args

The new `echo.yaml` file is a bit more complex, and it introduced too many new concepts.

You can notice that we are passing the params with the `args` field, you can also notice that we used `{{ params.message.as_arg }}` which is the equivalent of `--message={{ message }}`.

> **Note**: For more information about params, please check the [specification section](/docs/core/specification/params/)

## Explaining init

For the purpose of this example, we provided our program as an init file, we could have created a directory with this structure:

```
- echo-example/
  - echo.yaml
  - echo.py
```

Where the `echo.py` contains:

```python
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--message',
        type=str,
        default="Default message")

    args = parser.parse_args()

    print(args.message)
```

And the `echo.yaml` contains:

```yaml
version: 1.1
kind: component
inputs:
- name: message
  type: str
run:
  kind: job
  container:
    image: polyaxon/polyaxon-quick-start
    workingDir: "{{ globals.run_artifacts_path }}/uploads"
    command: [python3, -u, echo.py]
    args: ["{{ params.message.as_arg }}"]
```

In that case we could have used the `--upload/-u` flag to upload the code necessary for running the component:

```bash
polyaxon run -u -f echo.yaml -P message="test 1" -l
```

> **Note**: You can learn more about how to iterate with upload, git, and inline scripts in the [iterative process introduction section](/docs/intro/iterative-process/iterate-in-notebooks/).

## Multiple params

Let's extend the previous example to require multiple parameters:


```python
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--message1',
        type=str,
        default="Default message1")

    parser.add_argument(
        '--message2',
        type=str,
        default="Default message2")

    parser.add_argument(
        '--message3',
        type=str,
        default="Default message3")

    args = parser.parse_args()

    print(args.message1)
    print(args.message2)
    print(args.message3)
```


And the `echo.yaml` component:

```yaml
version: 1.1
kind: component
inputs:
- name: message1
  type: str
- name: message2
  type: str
- name: message3
  type: str
run:
  kind: job
  container:
    image: polyaxon/polyaxon-quick-start
    workingDir: "{{ globals.artifacts_path }}"
    command: [python3, -u, echo.py]
    args: ["{{ params.message1.as_arg }}", "{{ params.message2.as_arg }}", "{{ params.message3.as_arg }}"]
```

The updated component now has a longer `args` section, and based on the logic your building the args list could be longer.
If you are running Polyaxon v1.9.1 or higher, you can request all params as args in a single line:


```yaml
version: 1.1
kind: component
inputs:
- name: message1
  type: str
- name: message2
  type: str
- name: message3
  type: str
run:
  kind: job
  container:
    image: polyaxon/polyaxon-quick-start
    workingDir: "{{ globals.artifacts_path }}"
    command: [python3, -u, echo.py]
    args: "{{ params.as_args }}"
```

The value `"{{ params.as_args }}"` is equivalent to `["{{ params.message1.as_arg }}", "{{ params.message2.as_arg }}", "{{ params.message3.as_arg }}"]`.
