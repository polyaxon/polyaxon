---
title: "Events"
sub_link: "events"
meta_title: "Polyaxon Events - Polyaxon Automation Reference"
meta_description: "Events for subscribing operations to external events or internal triggers and conditions."
visibility: public
status: published
is_index: true
tags:
  - reference
  - polyaxon
  - polyflow
  - pipelines
  - dags
  - events
sidebar: "automation"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

## Overview

Events allow you to automate and extend certain aspects of Polyaxon's internal behavior and to integrate with external tools and systems.


## Use cases

Using events, users can subscribe operations to external events or internal triggers and conditions.

 * Usage in DAGs: instead of using the `trigger` field which waits for a final state of the upstream runs, users can define the exact status to trigger an operation.
 * Usage based on internal alerts: an operation can be attached to an internal alert to be triggered as soon as the internal condition is met.
 * Usage based on external triggers: an operation can wait for external events/hooks to be triggered.
