The Polyaxon tracking is a high level api for logging parameters, 
code versions, metrics, and outputs when running your machine learning code,
both on a Polyaxon deployment or on in a different platform/environment.

The tracked information will be later visualized and compared on the Polyaxon dashboard.

Polyaxon tracking lets you log and interact with REST API in a very convenient way.


In previous versions of Polyaxon, we only exposed metrics reporting through, [polyaxon-helper](polyaxon_helper).

The new polyaxon-client allows more advanced workflows, both manged by Polyaxon, in-cluster runs, or on external environment (e.g. your local machine).

This section will guide you how to track:

 * [Experiments](experiments)
 * [Jobs](jobs)
 * [Experiment Groups](experiment_groups)
 
In addition to this high level tracking APIs, when running an experiment/job inside Polyaxon, 
some paths and other information are exposed: 

 * [Paths](paths)

## Installation

```bash
$ pip install -U polyaxon-client
```

for python3

```bash
$ pip3 install -U polyaxon-client
```


## Installation in polyaxonfile

If you want to delegate the installation to polyaxon during the build process,
add a new step to the `run` section in your polyaxonfile:

```yaml
...
build:
  image: ...
  build_steps:
    - ...
    - pip install -U polyaxon-client
    - ...

run:
  cmd: ...
```
