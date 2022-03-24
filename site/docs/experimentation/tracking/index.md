---
title: "Polyaxon Tracking API"
sub_link: "tracking"
is_index: true
meta_title: "Polyaxon Tracking API Specification - Tracking - Experimentation"
meta_description: "Polyaxon Tracking API is a high-level API for logging parameters, code versions, metrics, and outputs when running your machine learning code, both on a Polyaxon deployment or on a different platform/environment."
visibility: public
status: published
tags:
  - client
  - api
  - polyaxon
  - python
  - tracking
  - reference
  - sdk
sidebar: "experimentation"
---

Polyaxon tracking is a high-level API for logging parameters,
code versions, metrics, and outputs when running your machine learning code,
both on a Polyaxon deployment or on a different platform/environment.

The tracked information will be later visualized and compared using [Polyaxon's UI](/docs/management/runs-dashboard/) or using other tools such as [Tensorboard](/docs/intro/tensorboard/single-tensorboard/).

Polyaxon tracking lets you log and interact with the REST API in a very convenient way,
the tracking module is an extension of the [Python client](/docs/core/python-library/run-client/)
so all information about installing the client and disabling the code related to Polyaxon can be found there.
It also means that you interact with [Polyaxon API](/docs/api/) in a programmatic way using all inherited methods.

In order to use Polyaxon Tracking API, the user must provide an authenticated client, if you are using the tracking module in-cluster,
it will be configured and authenticated automatically. There are several options to configure a client,
you can look at the [Python Library reference to learn more](/docs/core/python-library/#authentication).

> Although this section shows how to use Polyaxon tracking module, you can track experiments using any other language or directly by targeting [Polyaxon API](/docs/api/).

## Concepts

Polyaxon tracking exposes methods to log several aspects of a run:

 * Code Version: Git information used for the run.
 * Duration: Start and end time of the run.
 * Environment: Name of the file to launch the run, the command, arguments, Python packages, ...
 * Parameters: Key-value parameters used or this run.
 * Events & Metrics: Key-value metrics where the value is numeric. Each metric can be updated throughout the course of the run (for example, to track how your model’s loss function is converging), and Polyaxon records and lets you visualize the metric’s full history.
 * Outputs/Artifacts: Output files in any format. For example, you can record images, audio, models (e.g., a pickled scikit-learn model), or even data files (e.g. a Parquet file) as artifacts.

## Tracking in-cluster

When you start a run in-cluster you don't need to call several of  the exposed methods on the tracking reference
because they are recorded automatically, e.g. you don't need to set a name, description, tags, statuses, code reference
because they are saved during the creation of the experiment using the UI/CLI.


## Tracking references

Polyaxon exposes two flavors for tracking:

 * [tracking client reference](/docs/experimentation/tracking/client/)

 ```python
 from polyaxon.tracking import Run

 experiment = Run()
 experiment.log...
 ```

 * [tracking module reference](/docs/experimentation/tracking/module/)

 ```python
 from polyaxon import tracking

 tracking.init()
 tracking.log...
 ```
