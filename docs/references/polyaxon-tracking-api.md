---
title: "Polyaxon Tracking API"
sub_link: "polyaxon-tracking-api"
meta_title: "Polyaxon Tracking API Specification - Polyaxon References"
meta_description: "Polyaxon Tracking api is a high level api for logging parameters, code versions, metrics, and outputs when running your machine learning code, both on a Polyaxon deployment or on a different platform/environment."
visibility: public
status: published
tags:
    - tracking
    - reference
    - polyaxon
    - client
    - sdk
sidebar: "polyaxon-tracking-api"
---

Polyaxon tracking is a high level api for logging parameters, 
code versions, metrics, and outputs when running your machine learning code,
both on a Polyaxon deployment or on a different platform/environment.

The tracked information will be later visualized and compared on the Polyaxon dashboard.

Polyaxon tracking lets you log and interact with REST API in a very convenient way.


In previous versions of Polyaxon, we only exposed metrics reporting through, [polyaxon-helper](polyaxon_helper).

The new polyaxon-client allows more advanced workflows, both managed by Polyaxon, in-cluster runs, or on external environment (e.g. your local machine).

This section will guide you how to track:

 * [Experiments](/references/polyaxon-tracking-api/experiments/)
 * [Jobs](/references/polyaxon-tracking-api/jobs/)
 * [Experiment Groups](/references/polyaxon-tracking-api/experiment-groups/)
 
In addition to this high level tracking APIs, when running an experiment/job inside Polyaxon, 
some paths and other information are exposed: 

 * [Paths](/references/polyaxon-tracking-api/paths/)

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

## Disabling polyaxon tracking without changing the code

Since using the Polyaxon client and the tracking api requires code change, e.g.

```python
# Polyaxon experiment
experimet = Experiment()
# training code ...
# Metrics reporting
experiment.log_metrics(step=1000, loss=0.01, accuracy=0.97)
``` 

Users might need to run the same code outside of a Polyaxon context, 
which will break since Polyaxon related operations perform api calls.
  
Starting from **v0.3.8**, users won't need to perform any change to their code, 
they just need to set an environment variable `POLYAXON_NO_OP` to true/1, and the Polyaxon code will be ignored.   
