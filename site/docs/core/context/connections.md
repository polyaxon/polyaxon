---
title: "Context Connections"
sub_link: "context/connections"
meta_title: "Context Connections- Polyaxon Specification"
meta_description: "All connections requested by the main container and init containers will be exposed to the context as well along with theirs schemas."
visibility: public
status: published
tags:
  - specification
  - api
  - polyaxon
  - yaml
  - json
  - python
sidebar: "core"
---

## Overview

`connections` is the section that defines information about any connection requested by the main container or init containers. 

## Definition

All connections and their schemas, if they define one, will be available in the context as a dictionary: `{CONNECTION_NAME: SCHEMA_DEFINITION, ...}`.

> **Note** Not all connections have a schema, and just expose env vars or mount secret volumes.

Example:

```yaml
version: 1.1
kind: component
inputs:
- name: intput1
  type: str
- name: input2
  type: str

run:
  kind: job
  init:
  - connection: connection_with_schema
    container:
      image: "custom-container"
      command: ["echo"]
      args: ["{{ init[connection_with_schema].schemaKey }}"]
  connections: ["some_git_connection"]
  container:
    image: "image:test"
    command: ["command"]
    args: [
      "--param1={{ input1 }}",
      "--param2={{ input2 }}",
      "--param3={{ connections[some_git_connection].url }}"
    ]
```
You can see from the example above that we defined two connections, one is used in the init container `connection_with_schema` and one is requested by the main container `some_git_connection`.

In both cases, we are using the schema that those connections define. Both typed schemas and custom schemas behave the same way, and the user must know which key to request from the schema.
