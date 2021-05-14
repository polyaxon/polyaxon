---
title: "Executing Hooks"
sub_link: "automation/executing-hooks"
meta_title: "Executing Hooks - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Executing Hooks - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

> **Note**: This section of the tutorial can only run on Polyaxon EE and Polyaxon Cloud.

Hooks are a simpler abstraction than a DAG, and allows to trigger post-done component, like sending notifications or triggering a logic in response to the final state of an operation.
You can use any component as a hook, as long as it's registered in the public component hub or a private hub in your organization.

## Using the public components

Polyaxon provides several public components where the main purpose if to be used as a hook, like notifiers, for instance you can notify a slack channel about the state of your jobs:

```yaml
hooks:
  - trigger: succeeded
    hubRef: slack
    connection: slack-notification
```

If you need to receive notification for all done statuses:

```yaml
hooks:
  - trigger: done
    hubRef: slack
    connection: slack-notification
```

## Running multiple hooks

It's also possible to have multiple hooks or the same hook based on different conditions, for instance, 
a user can both send a slack notification and start a tensorboard after a successful experiment:

```yaml
hooks:
  - trigger: succeeded
    hubRef: tensorboard
    disableDefaults: true
    params:
      uuid: { value: '{{ globals.uuid }}' }
  - trigger: succeeded
    hubRef: slack
    connection: slack-notification
```
