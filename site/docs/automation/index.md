---
title: "Polyaxon automation tools"
sub_link: ""
meta_title: "Polyaxon automation engine: DAGs, workflow, matrix, parallelism, hyperparameter tuning, Schedules - Polyaxon Automation"
meta_description: "Polyaxon automation engine is a workflow management system that makes it easy to take your data pipelines or machine learning workflows and add semantics like retries, logging, dynamic mapping, caching, failure notifications, and more."
visibility: public
is_index: true
status: published
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

Polyaxon automation is a set of tools for:

   * [Authoring DAGs](/docs/automation/flow-engine/)
   * [Running hyperparameter tuning of ML models](/docs/automation/optimization-engine/)
   * [Running jobs and pipelines in parallel](/docs/automation/mapping/)
   * [Running components on schedule](/docs/automation/schedules/)
   * [Subscribing components to events](/docs/automation/helpers/)

## Features
 * Lineage: Strongly typed inputs and outputs for a full provenance of parameters and data.
 * Helpers: All workflows can be parameterized, cached by default, with pre-computed results, outputs, and artifacts.
 * Massive scale: Fully distributed, several scheduling strategies, controlled concurrency, fault-tolerant, scale to multiple nodes, clusters, and hundreds of thousands of concurrent executions.
 * Dynamic, customizable, and extensible: Use several runtimes in your graph of operations, experiments, jobs, services, distributed jobs, ...
