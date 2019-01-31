---
title: "Customize Run Environment"
sub_link: "custom-run-environment"
meta_title: "Customize run environment in Polyaxon - Configuration"
meta_description: "The following sections will describe how to use existing docker images and how to create custom images for your experiments' run environment."
tags:
    - configuration
    - polyaxon
    - kubernetes
    - environment
    - scheduling
    - orchestration
sidebar: "configuration"
---

<blockquote class="warning">This configuration is only available for Polyaxon deployed on Kubernetes clusters.</blockquote>

Usually a docker image specifies the functionality and environment
that you wish to run your experiments.

The following sections will describe how to use existing docker images and how to create custom images.

## Public images

You can use any docker image available on a public registry to run your experiments.

You can also build your custom docker images and push them to a public registry and use them on Polyaxon.


## Custom images

Alternatively, you can use the polyaxonfile to define how to customize a public image to your need,
and Polyaxon will take care of building the image before running your code.

For example

```yaml

---
version: 1

kind: experiment

declarations:
  batch_size: 128
  lr: 0.1

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn

run:
  cmd: python3 train.py --batch_size={{ batch_size }} --lr={{ lr }}
```

### Environment variables

To expose some environment variables you can use `env_vars`

For example

```yaml

---
version: 1

kind: experiment

declarations:
  batch_size: 128
  lr: 0.1

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn
  env_vars:
    - ['MY_ENV_VAR_KEY1', 'MY_ENV_VAR_VALUE1']
    - ['MY_ENV_VAR_KEY2', 'MY_ENV_VAR_VALUE2']

run:
  cmd: python3 train.py --batch_size={{ batch_size }} --lr={{ lr }}
```

### Installing libraries with pip

Polyaxon also provides, an easy way to install multiple python libraries:

 1. you can define a requirements file; the name must be either `requirements.txt` or `polyaxon_requirements.txt`


    ```bash
    $ vi polyaxon_requirements.txt
    ...
    ```

 2. a command `pip install -r polyaxon_requirements.txt` to install the requirements


    ```yaml
    ---
    version: 1

    kind: experiment

    declarations:
      batch_size: 128
      lr: 0.1

    build:
      image: tensorflow/tensorflow:1.4.1-py3
      build_steps:
        - pip install -r polyaxon_requirements.txt

    run:
      cmd: python3 train.py --batch_size={{ batch_size }} --lr={{ lr }}
    ```

### Installing other libraries or running other commands

You can also install or execute other commands, by adding them to the `build_steps` part.
If you have multiple commands that you wish to execute,
You can create an executable file, the filename must be `polyaxon_setup.sh` or `setup.sh`, and a command to execute that file `./polyaxon_setup.sh`.

```yaml

---
version: 1

kind: experiment

declarations:
  batch_size: 128
  lr: 0.1

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - ./polyaxon_setup.sh

run:
  cmd: python3 train.py --batch_size={{ batch_size }} --lr={{ lr }}
```


### Running multiple commands as a string

The `cmd` subsection accept either a string (1 command) or or list of strings (multiple commands)

This is all valid commands that Polyaxon will execute:


```yaml

---
...

run:
  cmd: cmd1 && cmd2 && cmd3
```
```yaml

---
...

run:
  cmd: cmd1 && cmd2 || cmd3
```
```yaml

---
...

run:
  cmd: cmd1 && cmd2; cmd3 || cmd4
```


### Running multiple commands as a list of strings

The `cmd` subsection accept either a string (1 command) or or list of strings (multiple commands)

This is all valid commands that Polyaxon will execute:


```yaml

---
...

run:
  cmd: 
    - cmd1
    - cmd2
    - cmd3
```

The resulting command passed to kubernetes will be a single command joined with `&&`: `cmd1 && cmd2 && cmd3`

### Running a script


In some cases you will need to execute a complex command, or multiple commands 
that could best run from an executable file,
e.g. `run.sh` where you will put all the commands you wish to execute, and then just run that file:

For example the `run.sh` could be:

```bash
cd to_some_path; echo "running my run.sh file"; python model.py
```

And your cmd in polyaxonfile:

```yaml
run:
  cmd: /bin/bash run.sh
```

### Custom configmaps and secrets


In some cases, users might need to authenticate to a third party service 
that the platform does not have an integration for yet, 
Polyaxon provides a way to mount custom config maps and secrets for your runs.

To be able to mount a config map or secret in your jobs/builds/experiments, 
you need to create the config map/secret, and add it to you deployment config:

For example:

```yaml
secretRefs: [secret1, secret2, secret3]
configmapRefs: [configmap1, configmap2, secret3]
```

During the scheduling of your build/job/experiment, 
you can reference the config map(s)/secret(s) that you want to mount in the environment section:

```yaml

environment:
  ...
  secret_refs: ['secret1', 'secret2']
  configmap_refs: ['configmap1', 'configmap3']
```
