---
title: "Manual Approval"
sub_link: "scheduling-strategies/manual-approval"
meta_title: "How to suspend operations and workflows until a user approves them - scheduling strategies"
meta_description: "A feature to pause and suspend operations and pipelines and wait for human approval to resume the work."
tags:
  - namespace
  - queueing
  - pipelines
  - kubernetes
  - scheduling
sidebar: "core"
---

## Overview

There are several situations when an operation or a pipeline might require some manual approval to continue.

Polyaxon provides a flag `isApproved: false` to perform human in the loop pattern. This flag can be set:
 * As default configuration on the [component level](/docs/core/specification/component/#isapproved).
 * On [per operation basis](/docs/core/specification/operation/#isapproved).
 * Via a [preset](/docs/core/scheduling-strategies/presets/).
 
In all these cases, if a run is decorated with this flag, the operation will be waiting and can only be resumed by an individual or event, either from the UI, the CLI, or the API.

## Suspending a pipeline

If an operation is defined in the context of a DAG and is decorated with `isApproved: false`, 
any branch that defines an upstream dependency on that operation will be suspended as a result of the dependency until the upstream operation is approved.
