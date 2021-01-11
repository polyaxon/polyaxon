---
title: "Joins"
sub_link: "joins"
meta_title: "Polyaxon Joins - Polyaxon Automation Reference"
meta_description: "Joins in Polyaxon allow to filter, aggregate, and annotate inputs/outputs/artifacts from multiple or parallel upstream runs based on query/sort/limit specification."
visibility: public
status: published
is_index: true
tags:
    - reference
    - polyaxon
    - polyflow
    - pipelines
    - dags
    - joins
sidebar: "automation"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

## Overview

Joins in Polyaxon allow to filter, aggregate, and annotate inputs/outputs/artifacts from multiple or parallel upstream runs based on query/sort/limit specification.


## Use cases

Using joins, users can dynamically initialize operations based on the inputs, outputs, and artifacts of runs based on a search specification.

 * Generate automatic reports based on query.
 * Start a tensorboard based on the top performing experiments in a project or a hyperparameter tuning pipeline.
 * Derive some analytics based on runs meeting some specific conditions or accessing some specific connection. 
