---
title: "Click"
meta_title: "Click"
meta_description: "Turn your programs to command-line applications with Click."
custom_excerpt: "Click is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary. It’s the “Command Line Interface Creation Kit”. It’s highly configurable but comes with sensible defaults out of the box."
image: "../../content/images/integrations/click.png"
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
[click](https://click.palletsprojects.com/) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.

## Creating a program

The following code is the default Python example program from the click package:

```python
import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")

if __name__ == '__main__':
    hello()
```

## Polyaxon component

```yaml
version: 1.1
kind: component
name: click-cli
inputs:
- name: count
  type: int
  isOptional: true
  value: 1
- name: name
  type: str
  isOptional: true
  value: World
run:
  kind: job
  container:
    image: polyaxon/polyaxon-examples:clis
    command: ["python", "cli.py"]
    args: ["{{ params.count.as_arg }}", "{{ params.name.as_arg }}"]

```

### Example as an executable component

> This inline example is intended to make it easy to execute this component without download or cloning any repo, this not intended as production pattern.

```yaml
version: 1.1
kind: component
name: click-cli
inputs:
- name: count
  type: int
  isOptional: true
  value: 1
- name: name
  type: str
  isOptional: true
  value: World
run:
  kind: job
  init:
    - file:
        filename: cli.py
        content: |
          import click
          
          @click.command()
          @click.option('--count', default=1, help='Number of greetings.')
          @click.option('--name', prompt='Your name',
                        help='The person to greet.')
          def hello(count, name):
              """Simple program that greets NAME for a total of COUNT times."""
              for x in range(count):
                  click.echo(f"Hello {name}!")
          
          if __name__ == '__main__':
              hello()
  container:
    image: polyaxon/polyaxon-examples:clis
    workingDir: "{{ globals.artifacts_path }}"
    command: ["python", "cli.py"]
    args: ["{{ params.count.as_arg }}", "{{ params.name.as_arg }}"]
```

## Scheduling the example

To schedule this component you can copy/past it to the UI and use the default values.

You can also schedule it with CLI:

```bash
polyaxon run -f cli.yaml -P count=4
```

To enable the sum flag

```bash
polyaxon run -f cli.yaml -P count=4 -P name="Your name"
```
