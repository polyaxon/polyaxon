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

> TIP. Although this section shows how to use Polyaxon tracking module, you can track experiments using any other language or directly by targeting Polyaxon API.

> N.B. If you are looking for the Python SDK to interact with Polyaxon API in a programmatic way, 
you need to check the [Polyaxon Python Client reference](/references/polyaxon-client-python/) instead.

> N.B. In previous versions of Polyaxon, we only exposed metrics reporting through, [polyaxon-helper](/references/polyaxon-tracking-api/polyaxon-helper/).

The new polyaxon-client allows more advanced workflows, both managed by Polyaxon, in-cluster runs, or on external environment (e.g. your local machine).

## Concepts

Polyaxon tracking allow track several aspect of a run, i.e. n experiment or a job:

 * Code Version: Git information used for the run.
 * Run time: Start and end time of the run.
 * Environment: Name of the file to launch the run, the command, arguments, python packages, ...
 * Parameters: Key-value parameters used or this run.
 * Metrics: Key-value metrics where the value is numeric. Each metric can be updated throughout the course of the run (for example, to track how your model’s loss function is converging), and lets you visualize the metric’s full history.
 * Outputs/Artifacts: Output files in any format. For example, you can record images, audio, models (e.g., a pickled scikit-learn model), or even data files (e.g. a Parquet file) as artifacts.

## Tracking reference

The [experiment tracking reference](/references/polyaxon-tracking-api/experiments) 
list a all methods exposed by this module, to learn more how you can use some or all of these methods in a specific context, 
please check the next section with practical [tracking guides](/references/polyaxon-tracking-api/#tracking-guides).

## Tracking guides

This section will help you use Polyaxon Tracking module:

 * In-cluster, i.e. experiments scheduled by Polyaxon inside a Kubernetes cluster

    For experiments and jobs running inside a cluster managed by Polyaxon, authentication is done automatically, i.e. you can create an instance of `Experiment` and `Job` 
    without providing any information, all information are setup automatically by Polyaxon.
     
     * [In-cluster Experiments tracking](/references/polyaxon-tracking-api/in-cluster-experiments/)
 
    If you are running a generic job and you wish to get information about that job inside your container
    
     * [In-cluster jobs tracking](/references/polyaxon-tracking-api/in-cluster-jobs/) 
        
 * On any platform not managed by Polyaxon, laptop, spark, sagemaker, colab, ...
    
     For experiments and jobs running outside a cluster managed by Polyaxon, this guide will show you how to authenticate and track experiments.  
     
     * [Other environments Experiments tracking](/references/polyaxon-tracking-api/other-environments/)
 


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

## Installation in Dockerfile

```dockerfile
RUN pip install -U polyaxon-client
```

## Disabling Polyaxon tracking without changing the code

Since using the Polyaxon client and the tracking api requires code change, e.g.

```python
# Polyaxon experiment
experiment = Experiment()
# training code ...
# Metrics reporting
experiment.log_metrics(step=1000, loss=0.01, accuracy=0.97)
``` 

Users might need to run the same code outside of a Polyaxon context, 
which will break since Polyaxon related operations perform api calls.
  
Starting from **v0.3.8**, users won't need to perform any change to their code, 
they just need to set an environment variable `POLYAXON_NO_OP` to true/1, and the Polyaxon code will be ignored.   
