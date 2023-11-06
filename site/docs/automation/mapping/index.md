---
title: "Mapping"
sub_link: "mapping"
meta_title: "Polyaxon Mapping - Polyaxon Automation"
meta_description: "Polyaxon mapping is a tool for applying a list of params combination to a component."
visibility: public
status: published
is_index: true
tags:
  - reference
  - polyaxon
  - polyflow
  - pipelines
  - dags
  - experimentation
sidebar: "automation"
---

## Overview

Polyaxon mapping is an automation tool to apply a list of parameters combination to a component sequentially or in parallel following a concurrency.

When a mapping is defined a pipeline is created to watch the generated executions and manage their lifecycle and concurrency.
Because the mapping generates a pipeline, the [pipeline helpers](/docs/automation/helpers/) can be used for managing concurrency, early stopping, caching, ...

 * [Mapping specification](/docs/automation/mapping/specification/) for more details
 * [Pipeline Helpers](/docs/automation/helpers/) for more information about the helpers that can be used with mapping


## Use cases

Polyaxon Mapping can be used to:
 * Run a component in parallel using a user defined list of parameters
 * Train a machine learning model using an external optimization and suggestion service
 * Leverage a map/reduce style pattern
