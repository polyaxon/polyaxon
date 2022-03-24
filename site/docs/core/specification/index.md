---
title: "Polyaxonfile Specification"
sub_link: "specification"
meta_title: "Polyaxonfile Specification - Polyaxon References"
meta_description: "In order to use Polyaxon, users need to create YAML/Json Polyaxonfiles. These files use a specification to describe how experiments, experiment groups, jobs, plugins should run on Polyaxon."
visibility: public
status: published
is_index: true
tags:
  - specifications
  - polyaxon
  - yaml
sidebar: "core"
---

## Overview

In order to schedule runs on Polyaxon, users need to create Polyaxonfiles.

![polyaxonfile architecture](../../../../content/images/references/specification/polyaxonfile.png)

These files use a specification to describe how jobs, distributed jobs, services, parallel executions, and pipelines should run on Polyaxon.

The Polyaxonfile specification can be authored in YAML, json, python, and partially in Go, Typescript, and Java. 
This specification is based on a list of sections, in this guide, we describe the required and optional sections.

## Primitives

The main primitives that the user will be interacting with are:

 * [Component](/docs/core/specification/component/): A discrete, repeatable, and self-contained action that defines an environment and a runtime.
 * [Operation](/docs/core/specification/operation/): This is how Polyaxon operationalizes and executes a component by passing parameters, connections, and possibly patch the run environment.

Polyaxon can resolve the content of a Polyaxonfile based on 2 information:

 * version: this is the version of the specification file, all Polyaxon components (CLI, Clients, API, Compiler, Operation) rely on this information to know how to parse the content using the versioned schema.
    ```yaml
    version: 1.1
    ...
    ```
 * kind: this is the kind of the specification file, the possible values are `component` and `operation`.
