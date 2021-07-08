---
title: "Python Fire"
meta_title: "Python Fire"
meta_description: "Turn your programs to command-line applications with Python Fire."
custom_excerpt: "Python Fire is a library for automatically generating command line interfaces (CLIs) from absolutely any Python object."
image: "../../content/images/integrations/python.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - cli
featured: false
popularity: 0
class_name: instruction
visibility: public
status: examples
---

Polyaxon schedules containers using typed components with inputs and outputs, oftentimes users will need to create and expose their programs as command-line applications.
[Python Fire](https://github.com/google/python-fire) is a library for automatically generating command line interfaces (CLIs) from absolutely any Python object.

## Creating a program

The following code is the default Python example program from the Python fire package:

```python
import fire
from polyaxon import tracking

class Calculator:
    """A simple calculator class."""

    def double(self, number):
        results = 2 * number
        tracking.log_outputs(results=results)
        return results

if __name__ == '__main__':
    tracking.init()
    fire.Fire(Calculator)
```

## Polyaxon component

```yaml
version: 1.1
kind: component
name: fire-cli
inputs:
- name: number
  type: int
  isOptional: true
  value: 10
outputs:
- name: results
  type: int
run:
  kind: job
  container:
    image: polyaxon/polyaxon-examples:clis
    command: ["python", "cli.py", "double"]
    args: ["{{ number }}"]
```

or 

```yaml
version: 1.1
kind: component
name: fire-cli
inputs:
- name: number
  type: int
  isOptional: true
  value: 10
outputs:
- name: results
  type: int
run:
  kind: job
  container:
    image: polyaxon/polyaxon-examples:clis
    command: ["python", "cli.py", "double"]
    args: ["{{ params.number.as_arg }}"]
```

### Example as an executable component

> This inline example is intended to make it easy to execute this component without download or cloning any repo, this not intended as production pattern.

```yaml
version: 1.1
kind: component
name: fire-cli
inputs:
- name: number
  type: int
  isOptional: true
  value: 10
outputs:
- name: results
  type: int
run:
  kind: job
  init:
    - file:
        filename: cli.py
        content: |
          import fire
          from polyaxon import tracking
          
          class Calculator:
              """A simple calculator class."""
          
              def double(self, number):
                  results = 2 * number
                  tracking.log_outputs(results=results)
                  return results
          
          if __name__ == '__main__':
              tracking.init()
              fire.Fire(Calculator)
  container:
    image: polyaxon/polyaxon-examples:clis
    workingDir: "{{ globals.artifacts_path }}"
    command: ["python", "cli.py", "double"]
    args: ["{{ number }}"]
```

## Scheduling the example

To schedule this component you can copy/past it to the UI and use the default values.

You can also schedule it with CLI:

```bash
polyaxon run -f cli.yaml -P number=4
```
