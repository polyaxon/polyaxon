---
title: "Iterate with inline scripts"
sub_link: "iterative-process/iterate-with-inline-scripts"
meta_title: "Running inline scripts - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Often, users want to just execute a script specified as a here-script (also known as a here-doc) in their operation"
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

Sometime users may want to execute a script in their operation or to generate a file that can be used as an input for an init container or the main container without cloning a repo.


## Running a python script

This example shows how to initialize a python script without cloning a repo or uploading code:

```yaml
version: 1.1
kind: component
run:
  kind: job
  init:
    - file:
        content: |
          print("Hello World")
        filename: script.py
  container:
    image: polyaxon/polyaxon-quick-start
    workingDir: "{{ globals.artifacts_path }}"
    command: [python3, -u, script.py]
```

This example creates a file `script.py` in the init section and executes it in the main container.

Similar to all other init containers, we could provide a custom path where the file should be initializer:

```yaml
init:
  - file:
      content: |
        print("Hello World")
      filename: script.py
    path: custom/path/to/use
```


## Running a bash script

```yaml
version: 1.1
kind: component
run:
  kind: job
  init:
    - file:
        content: |
          echo 'This is a test.' | wc -w
        filename: script.sh
        chmod: "+x"
  container:
    image: polyaxon/polyaxon-quick-start
    workingDir: "{{ globals.artifacts_path }}"
    command: ['/bin/bash', '-c']
    args: ['./script.sh']
```


## Initializing a YAML file

```yaml
version: 1.1
kind: component
run:
  kind: job
  init:
    - file:
        content: |
          version: 1.1
          kind: component
          run:
            kind: job
            init:
              - file:
                  content: |
                    echo 'This is a test.' | wc -w
                  filename: script.sh
                  chmod: "+x"
            container:
              image: polyaxon/polyaxon-quick-start
              workingDir: "{{ globals.artifacts_path }}"
              command: ['/bin/bash', '-c']
              args: ['./script.sh']
        filename: polyaxonfile.yaml
        chmod: "+x"
  container:
    image: polyaxon/polyaxon-cli
    workingDir: "{{ globals.artifacts_path }}"
    command: ['polyaxon', "check", '-f']
    args: ['polyaxonfile.yaml']
```
