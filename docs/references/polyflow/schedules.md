---
title: "Polyflow: Schedules"
sub_link: "schedules"
meta_title: "Polyaxon Polyflow: Schedules - Polyaxon References Polyaxon"
meta_description: "To be able to trigger a pipeline repeatedly, a pipeline must define a schedule. Polyflow provides 2 ways to define a schedule to automate the process of creating pipeline runs."
visibility: public
status: published
tags:
    - reference
    - polyaxon
    - polyflow
    - pipelines
    - dags
    - experimentation
sidebar: "polyflow"
---

> Polyflow is in beta, please reach out to us if you want to have early access


## Overview

Polyaxon monitors all tasks and all DAGs, and triggers ops whose dependencies have been met. 

Pipelines are by default triggered one time, or as many times as the users trigger a new run.

To be able to trigger a pipeline repeatedly, a pipeline must define a schedule. Polyflow provides 2 ways to define a schedule to automate the process of creating pipeline runs.

## Interval schedules

A simple schedule is the interval schedule:

 * kind: interval
 * start_at: `optional`
 * end_at: `optional`
 * frequency: `required` / `str`
 * depends_on_past: `bool`


## Cron schedules

Cron schedule accepts a cron expression to create pipeline runs:

 * kind: cron
 * start_at: `optional`
 * end_at: `optional`
 * cron: `required` / `str`
 * depends_on_past: `bool`
