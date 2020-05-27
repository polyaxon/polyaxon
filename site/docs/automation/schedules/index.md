---
title: "Schedules"
sub_link: "schedules"
meta_title: "Polyaxon Schedules - Polyaxon Automation Reference"
meta_description: "To be able to trigger a component repeatedly, a pipeline must define a schedule."
visibility: public
status: published
tags:
    - reference
    - polyaxon
    - polyflow
    - pipelines
    - dags
    - schedules
sidebar: "automation"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

## Overview
 
Components are by default triggered one time when a user create an operation, 
or as many times as the users trigger new operations.
Polyaxon monitors all operations and all DAGs, and triggers ops whose dependencies have been met.

To be able to trigger components repeatedly, the operation must define a schedule. 
Polyaxon provides several scheduling interfaces to automate the process of creating runs.
 
 * [Cron schedules](/docs/automation/schedules/cron/)
 * [Interval schedules](/docs/automation/schedules/interval/)
 * [Repeatable schedules](/docs/automation/schedules/repeatable/)
 * [Exact time schedules](/docs/automation/schedules/exact-time/)
