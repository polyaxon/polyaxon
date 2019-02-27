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

### Using dockerfile instead of the build section details

In many cases, defining all steps needed to create an image might require information that polyaxonfile' specification does not provide, 
in that case we ask users to define their own Dockerfile(s) and use them to create containers for jobs and experiments:

```yaml
version: 1

kind: experiment

build:
  dockerfile: path/to/Dockerfile
```

The Dockerfile must be part of the project repo.


### Defining build context

Assuming your project has the following structure:

```
/mnist
    |_ dockerfiles
        |_ DockerfileJob
        |_ DockerfileExperiment
    |_ module1
        |_ main.py
        |_ preprocess.py
        |_ exec.sh
    |_ modeule2
        |_ main.py
        |_ model.py
```

You might want to mount `mudule1` to a job to do some preprocessing, and `module2` to an experiment to train a model:

Job:

```yaml
version: 1

kind: job

build:
  dockerfile: dockerfiles/DockerfileJob
  context: module1

run:
  cmd: exec.sh
```

Experiment1:

```yaml
version: 1

kind: experiment

build:
  dockerfile: path/to/DockerfileExperiment
  context: module2

run:
  cmd: python3 main.py --arg1=foo --arg2=bar
```

Experiment2:

```yaml
version: 1

kind: experiment

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install -r polyaxon_requirements.txt
  context: module2
  backend: kaniko

run:
  cmd: python3 main.py --arg1=foo --arg2=bar
```

### Disabling the cache during the build process

Often times users might need to force rebuilding an image or just discard the cache, this is possible by adding `nocache` to the build section:


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
  nocache: true
```

### Changing the build backend

Polyaxon supports multiple build backends, by default Polyaxon uses a built-in native builder, however you can change the build process either per job/experiment, 
or change set the default backend to use for all builds. Please check the currently supported [build backends](/integrations/containers/).

### Running multiple commands as a string

The `cmd` subsection accept either a string (1 command) or or list of strings (multiple commands)

This is all valid commands that Polyaxon will execute:


```yaml
...

run:
  cmd: cmd1 && cmd2 && cmd3
```
```yaml
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

## Custom configmaps and secrets


In some cases, users might need to authenticate to a third party service 
that the platform does not have an integration for yet, 
Polyaxon provides a way to mount custom config maps and secrets for your runs.

To be able to mount a config map or secret in your jobs/builds/experiments, 
you need to create the config map/secret in the namespace of your Polyaxon 
deployment and add it to you deployment config:

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

Within your build/job/experiment the individual items of your secrets are then exposed
as environment variables. As an example, requiring a secret with the following data section

```yaml
data:
  test_user: <base64>
  test_password: <base64>
```

would expose `test_user` and `test_password` environment values containing the decoded values.

## Custom resources

You can customize your container's resources, by providing a resources subsection to the environment's section: 

```yaml
environment:
  resources:
    cpu:
      requests: 1
      limits: 2
    memory:
      requests: 256
      limits: 1024
```

### Using GPUs

To use GPUs you can use the same subsection to request GPUs

```yaml
environment:
  resources:
    cpu:
      requests: 1
      limits: 2
    memory:
      requests: 256
      limits: 1024
    gpu:
      request: 1
      limits: 1
```


### Using TPUs

To use TPUs, you need to deploy Polyaxon on GKE, and have a tensorflow version compatible with TPU:

```yaml
environment:
  resources:
    cpu:
      requests: 1
      limits: 2
    memory:
      requests: 256
      limits: 1024
    tpu:
      request: 8
      limits: 8
```

Polyaxon uses `cloud-tpus.google.com/v2` as a default resource key and `1.12` as default Tensorflow TPU version, but you can change this values in your deployment config file:

```yaml
tpuResourceKey: "cloud-tpus.google.com/preemptible-v2"  # To use preemptible TPU
tpuTensorflowVersion: "1.11"  # To use Tensorflow 1.11 version
```
