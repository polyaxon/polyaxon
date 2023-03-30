---
title: "Python Library"
sub_link: "python-library"
meta_title: "Introduction to the Python Library - Python Client References"
meta_description: "Use our Python library to instrument your machine learning model and track experiments, create Polyaxonfile specification, and extend Polyaxon's behavior. Setup should only take a few lines of code. If you're using a popular framework, we have several integrations to make setting up Polyaxon easy."
visibility: public
status: published
tags:
  - client
  - api
  - polyaxon
  - python
sidebar: "core"
---

## Overview

Polyaxon's Python library is a high level Python module, you can use it to:
  * create Polyaxonfile specification.
  * to interact with Polyaxon API in a programmatic way.
  * to instrument your machine learning model and track experiments.
  * create custom visualizations.
  * to extend Polyaxon's behavior.

## Install

```bash
pip install -U polyaxon
```

## CLI

[Polyaxon CLI](/docs/core/cli/) is a tool and a client to interact with Polyaxon, it allows you to manage your cluster, projects, and experiments.

## Clients

This module includes a client that can be used to interact with Polyaxon API in a programmatic way.


 * [Client Reference](/docs/core/python-library/polyaxon-client/): Auto-configurable and high-level base client that abstract the need to set a configuration for each service.
 * [Project Client](/docs/core/python-library/project-client/): A client to communicate with Polyaxon projects endpoints.
 * [Run Client](/docs/core/python-library/run-client/): A client to communicate with Polyaxon runs endpoints.

## Tracking Client

The [tracking client](/docs/experimentation/tracking/) is an extension and a subclass
of the [Run Client](/docs/core/python-library/run-client/) with more methods for machine learning experiment tracking.

## Run Plot client

The [RunPlot and MultiRunPlot classes](/docs/experimentation/visualizations/) are also extensions and a subclasses
of the [Run Client](/docs/core/python-library/run-client/) with more functionalities
to drive visualization programmatically using [Plotly Express](https://plotly.com/python/plotly-express/) and [HiPlot](https://github.com/facebookresearch/hiplot).
