---
title: "Passing params with environment variables"
sub_link: "passing-params/with-env-vars"
meta_title: "Passing parameters to your programs as environment variables - Core Concepts"
meta_description: "Passing parameters to your programs as environment variables requires that you set the proper handling of environment variables in your programs."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

Passing parameters as environment variables requires that you set the proper handling of environment variables in your programs.

## Overview

Oftentimes you will need to expose an input or a context meta data as an environment variable, 
in some other situations you might want to skip creating a CLI to run a program and handle the logic based on the environment variables exposed in the system.

Polyaxon exposes the full [Kubernetes container specification](https://kubernetes.io/docs/concepts/containers/), which means that you can leverage the `env` sub-section to expose environment variables:

## Example

Let's look at a simple program that just prints some information based on an environment variable:

```python
import os

if __name__ == '__main__':
    print(os.environ.get("INPUT_MESSAGE", "Default message"))
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
          import os

          if __name__ == '__main__':
              print(os.environ.get("INPUT_MESSAGE", "Default message"))
              
        filename: echo.py
  container:
    image: polyaxon/polyaxon-quick-start
    workingDir: "{{ globals.artifacts_path }}"
    command: [python3, -u, echo.py]
    env:
      - name: INPUT_MESSAGE
        value: "{{ message }}"
```

Now you can run multiple version of this example:

```bash
polyaxon run -f echo.yaml -P message="test 1" -l
```

```bash
polyaxon run -f echo.yaml -P message="test 2" -l
```

## Exposing inputs/outputs to env var

> **N.B**: Requires CLI `>= v1.12`.

To improve the previous process, Polyaxon IO/Params specification has an option to expose the value to an environment variable automatically.
Instead of manually using the configuration:

```yaml
    env:
      - name: INPUT_MESSAGE
        value: "{{ message }}"
```

It's possible to use the specification `toEnv` to tell Polyaxon to expose the variable:

```yaml
inputs:
- name: message
  type: str
  isOptional: true
  value: "Default message"
  toEnv: INPUT_MESSAGE  # <----
```

`toEnv` is also available on the params specification, in case the component does not define if the IO should expose the value to an env var, 
or in case a param is used as context only:

```yaml
params:
  message:
    value: "New message"
    toEnv: ENV_VAR_MESSAGE  # <----
```
