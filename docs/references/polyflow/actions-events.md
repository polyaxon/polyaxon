---
title: "Polyflow: Actions/Events"
sub_link: "polyflow"
meta_title: "Polyaxon Polyflow: Actions/Events - Polyaxon References Polyaxon"
meta_description: "Actions/Events are self contained components that can be used by any user of Polyaxon perform an operation"
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

Actions/Events are self contained Polyaxonfiles where every parameter passed should be checked against an input/output, and packaged with minimal code required to run the Action/Event.

An action is essentially a self-contained experiment or job to perform a specific generic action, and can be invoked by any pipeline running in any project in a Polyaxon deployment.

An event is essentially a self-contained job that waits for an event, or a for a certain time, for a file, or for a database entry, ...

## Specification

Actions and events are similar to a [template](/references/polyflow/templates/) and use the same specification, but are packaged with a code to perform the action/event, 
i.e. they don't depend on the current context of the project's code.

A typical structure of an action/event:

 * `polyaxonfile.yaml`: to define the specification of the action/event.
 * `action-entrypoint`: this could be for example: `main.py` or `task.py` if the code is in python, but an action can be developed in any language. 
 * `code/`: additional code used for the action logic.

## Registry

Polyflow's global registry contains some reusable actions/events for downloading/uploading data from S3/GCS/Azure, pulling data from hive, starting a Spark job, ...

Additionally, Polyaxon users can distributed their own actions/events:
 * CE edition: admins can register actions/events that can be used cluster wide.
 * EE edition: in addition to a global actions/events registry, you can distribute specific actions/events to registries scoped by teams.

## Distributing actions/events

Polyflow repo contains all public actions/events with their code, they are already built and distributed. We welcome users to make PRs to extend the list of reusable actions/events.

If you want to create actions/events specific to your company, the idea is simple you can create a repo containing the logic, see specification, and call `polyaxon action create /my-action` / `polyaxon event create /my-event`.

Polyaxon will package the action/event, create a the necessary container, and add it to the index to be used in your pipelines.

Once an action/event is distributed, users can use them in the pipelines: 
 * Actions: `template: {action: my-action-name}`
 * Events: `template: {event: my-event-name}`
 
