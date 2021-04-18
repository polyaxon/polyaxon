---
title: "Hooks"
sub_link: "hooks"
meta_title: "Polyaxon Hooks - Polyaxon Automation Reference"
meta_description: "To send generic webhooks, you just need to set the urls that you want to send webhooks to and the http methods to use."
visibility: public
status: published
is_index: true
tags:
  - reference
  - polyaxon
  - polyflow
  - pipelines
  - dags
  - hooks
sidebar: "automation"
---

<blockquote class="commercial">This is currently available on Polyaxon Cloud only.</blockquote>

## Overview

The Hooks section is an automation feature that allows to trigger an operation as soon as the main logic reaches a final state.
Although users can use any component as a hook, they should only restrict usage of hooks to recurrent logic, like notifications, 
that only makes sense in the context of the lifecycle of the main operation.

## Use cases

Hooks can be used to:
 * Notify external system about the results of operations.
 * Perform post-done analysis.
 * Generate reports or trigger validation/test of successful training operation.
 * Trigger a pipeline on a different infrastructure.

## Limitation

Compared to DAGs, Hooks have no concurrency management and can only trigger if a final state is met.
When an operation defines a list of hooks, Polyaxon will fan-out all hooks that validate their trigger and conditions. 
If you need to manage priority or concurrency, or throttle some hook types, you can assign them to specific queues. 

## Available events

|Event|Description|
|-----|-----------|
|`done`|Triggered whenever a run reached a done status|
|`succeeded`|Triggered whenever a run experiment succeeds|
|`failed`|Triggered whenever a run experiment fails|
|`stopped`|Triggered whenever a run experiment is stopped|
