---
title: "Extensions"
sub_link: "extensions"
meta_title: "Polyaxon Actions, Events, and Hooks - Polyaxon Automation Reference"
meta_description: "Extend Polyaxon with actions, events, and hooks."
visibility: public
status: published
is_index: true
tags:
    - reference
    - polyaxon
    - polyflow
    - pipelines
    - dags
    - schedules
sidebar: "automation"
---


Extensions allow you to automate and extend certain aspects about Polyaxon's internal behavior and to integrate with external tools and systems.


 * [Actions](/docs/automation/extensions/actions/): to extend Polyaxon UI and CLI, you can set actions on your operations. Every action is a reference to a component that can be executed based on the context of the operation where it's defined.
 * [Hooks](/docs/automation/extensions/hooks/): for sending webhooks and alerts on Slack/Discord/... when a job fails, succeeds, stops... and integrating with external systems.
 * [Events](/docs/automation/extensions/events/): for subscribing operations to external events or internal triggers and conditions.
