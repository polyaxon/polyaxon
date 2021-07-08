---
title: "Argparse"
meta_title: "Argparse"
meta_description: "Turn your programs to command-line applications with argparse Python module."
custom_excerpt: "The argparse module makes it easy to write user-friendly command-line interfaces."
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
The [argparse](https://docs.python.org/3/library/argparse.html) module makes it easy to write user-friendly command-line interfaces.

## Creating a program

The following code is the default Python example program from the argparse module, it takes a list of integers and produces either the sum or the max:

```python
import argparse
from polyaxon import tracking

tracking.init()

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                  help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                  const=sum, default=max,
                  help='sum the integers (default: find the max)')

args = parser.parse_args()
tracking.log_outputs(results=args.accumulate(args.integers))
```

## Polyaxon component

```yaml
version: 1.1
kind: component
name: argparse-cli
inputs:
- name: integers
  type: int
  isList: true
  isOptional: true
  value: [1, 2, 3, 4]
- name: sum
  type: bool
  isOptional: true
  isFlag: true
  value: false
outputs:
- name: results
  type: int
run:
  kind: job
  container:
    image: polyaxon/polyaxon-examples:clis
    workingDir: "{{ globals.artifacts_path }}"
    command: ["sh", "-c"]
    args: ["python cli.py {{ integers|map('string')|join(' ') }} {{ sum }}"]

```

### Example as an executable component

> This inline example is intended to make it easy to execute this component without download or cloning any repo, this not intended as production pattern.

```yaml
version: 1.1
kind: component
name: argparse-cli
inputs:
- name: integers
  type: int
  isList: true
  isOptional: true
  value: [1, 2, 3, 4]
- name: sum
  type: bool
  isOptional: true
  isFlag: true
  value: false
outputs:
- name: results
  type: int
run:
  kind: job
  init:
    - file:
        filename: cli.py
        content: |
          import argparse
          from polyaxon import tracking

          tracking.init()

          parser = argparse.ArgumentParser(description='Process some integers.')
          parser.add_argument('integers', metavar='N', type=int, nargs='+',
                              help='an integer for the accumulator')
          parser.add_argument('--sum', dest='accumulate', action='store_const',
                              const=sum, default=max,
                              help='sum the integers (default: find the max)')

          args = parser.parse_args()
          tracking.log_outputs(results=args.accumulate(args.integers))
  container:
    image: polyaxon/polyaxon-examples:clis
    workingDir: "{{ globals.artifacts_path }}"
    command: ["sh", "-c"]
    args: ["python cli.py {{ integers|map('string')|join(' ') }} {{ sum }}"]
```

## Scheduling the example

To schedule this component you can copy/past it to the UI and use the default values.

You can also schedule it with CLI:

```bash
polyaxon run -f cli.yaml -P integers=4,5,6,25
```

To enable the sum flag

```bash
polyaxon run -f cli.yaml -P integers=4,5,6,25 -P sum=true
```
