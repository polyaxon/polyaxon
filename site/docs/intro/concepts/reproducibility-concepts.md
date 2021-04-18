---
title: "Reproducibility Concepts"
sub_link: "concepts/reproducibility-concepts"
meta_title: "Polyaxon makes your experiments reproducible, portable, and repeatable while being language and framework agnostic. - Core Concepts"
meta_description: "Polyaxon makes your experiments reproducible, portable, and repeatable while being language and framework agnostic."
visibility: public
status: published
tags:
  - architecture
  - concepts
  - polyaxon
sidebar: "intro"
---

Reproducibility is a challenging problem in Machine Learning, it's the concept of being able to recreate a machine learning workflow or experiment and reach the same results.

Polyaxon makes your experiments reproducible, portable, and repeatable while being language and framework agnostic.

### Packaging Format

Every operation in Polyaxon is authored using a powerful specification and packaging format `Polyaxonfile`.

Polyaxonfile is a specification for packaging dependencies, inputs, outputs, artifacts, environments, and runtime of an operation to schedule on Kubernetes.

<blockquote class="light">Please refer to <a href="/docs/core/specification/">Polyaxonfile specification</a> for more details.</blockquote>

### Tracking

Polyaxon comes with a built-in extensive tracking system. You can log information for source code, parameters, data, metrics, tags, and logs using Polyaxon APIs or clients.
<blockquote class="light">Please refer to <a href="/docs/experimentation/tracking/">the tracking API</a> for more details.</blockquote>

### Lineage

Every operation scheduled with Polyaxon will be auto-documented with lineage information about its inputs and outputs, statuses, metrics, hyperparams, source code, data, visualizations, artifacts, and resources used in each experiment.

Polyaxon provides a dashboard and a CLI to see the full history at a glance, including when, who, and where,
as well as an advanced insight and comparison of experiments based on results, hyperparams, versions of training data, and source code.

<blockquote class="light">Please refer to <a href="/docs/management/runs-dashboard/">the runs dashboard</a> for more details.</blockquote>

