---
title: "Scheduling Concepts"
sub_link: "concepts/scheduling-concepts"
meta_title: "Polyaxon Scheduling/Schedules/Events/Actions/Agents/Queues - Core Concepts"
meta_description: "Polyaxon can trigger execution manually or automatically using schedules, data, and events driven strategies."
visibility: public
status: published
tags:
  - architecture
  - concepts
  - polyaxon
sidebar: "intro"
---

Polyaxon relies on a set of concepts to schedule and manage the lifecycle of operations.
In this section, we provide a high-level introduction to these concepts,
with more details in pages dedicated to each concept.

### Manual process

Often times users will drive the machine learning experimentation and iteration process manually.
Polyaxon provides several APIs, clients, UI, and CLI commands to submit and monitor operations.

### Schedules

Although you can run your operations at any time, for any reason, it is often useful to automate and run your components at certain times using a `schedule`.

Schedules provide a time-based mechanism to drive scheduling on Polyaxon, and can be used to automate:
 * Periodic execution (Distributed Cron)
 * Interval execution
 * Repeatable execution
 * Exact time execution

<blockquote class="light">Please refer to <a href="/docs/automation/schedules/">automation/schedules</a> for more details.</blockquote>

### Events

Many machine learning workflows make more sense to be triggered by listening to multiple event sources and execute actions if some state is reached:

 * Based on a new commit.
 * Based on data availability.
 * Based on metrics.

Polyaxon is a good fit for many of these use cases and it has direct support for asynchronous events (aka signals).

There are two ways to achieve event-driven scheduling:
 * You can make Polyaxon listen to events and schedule submissions based on certain conditions. (This is WIP)
 * Executing a periodic action checking for a state change (Polling).
 * You can build a logic to submit jobs based on the state of upstream systems: e.g. [Github Action](/integrations/github-action/).

### Triggers, Conditions, and Early Stopping

Polyaxon ships with a built-in automation engine (Flow engine & Optimization engine) to build your machine learning workflows.

Each DAG or Hyperparameter tuning operation can leverage a set of automation features:
 * Concurrency management
 * Caching
 * Early stopping
 * Conditions

<blockquote class="light">Please refer to <a href="/docs/core/specification/operation/">core/specification/operation</a> for more details.</blockquote>

### Agents/Queues

When submitting jobs manually or based on external events or internal triggers, you will be faced with questions related to queuing and scheduling.

Polyaxon provides several interfaces designed to achieve fairness when a limited resource is shared, for example, to prevent a hyperparameter tuning with large search space or parallel executions from consuming more cluster resources than other workflows and operations.

<blockquote class="light">Please refer to <a href="/docs/core/scheduling-strategies/">Scheduling strategies</a> for more details.</blockquote>

### Presets

`Presets` allows users to extract generic aspects of their polyaxonfiles and apply them using the override argument `-f` to automatically extend the configuration of their operations. 

`Presets` allows admins to preset several meta information about runs, e.g. node scheduling and routing, which facilitate attaching quotas to a user/team/project,
so that the entities they create, i.e. builds/jobs/experiments/notebooks, cannot exceed the parallelism and may not consume more
resources than the quota specification allows.

<blockquote class="light">Please refer to <a href="/docs/core/scheduling-presets/">scheduling-presets</a> and <a href="/docs/management/organizations/presets/">management/presets</a> for more details.</blockquote>
