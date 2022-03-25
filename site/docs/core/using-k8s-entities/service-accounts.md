---
title: "How to use a custom service account"
sub_link: "using-k8s-entities/service-accounts"
meta_title: "A guide on using a custom service for running operations - Core Concepts"
meta_description: "All pods managed by Polyaxon use the default service account created during the deployment of Polyaxon CE or Polyaxon Agent, however you can use specific service accounts on per operation level."
visibility: public
status: published
tags:
  - specification
  - api
  - polyaxon
  - yaml
  - json
  - python
  - concepts
sidebar: "core"
---

## Overview

All pods managed by Polyaxon use the default service account created during the deployment of Polyaxon CE or Polyaxon Agent.
This service account provides the necessary access to run operations using the default configuration, 
however, you may need to use a specific service account for some operations.

The amount of access which an operation need is dependent on what you need to achieve.
For example, if you need to create a component that creates other Kubernetes resources, a volume claim or a config map, 
then the default service account will prevent any operation using this component from successfully running. 
Such a component will require 'create' privileges on any resource that it needs to create.

## Usage

In order to provide a custom service account, you can leverage the environment section:

```yaml
kind: component
...
run:
  kind: ...
  environment:
    serviceAccountName: custom-sa
```

If you are running a distributed operation, you can provide a service account per replica.

## Reference

For more details about providing a service account compatible with Polyaxon auxiliary containers, 
please check the [service account specification](/docs/core/specification/environment/#serviceaccountname) in the environment section.

> **Note**: Although you can grant any access rights to your service account, especially if you disable Polyaxon sidecar and Polyaxon init containers, 
> we suggest that you read the minimum RBAC rules used in the default [service account](/docs/core/specification/environment/#serviceaccountname). 

## Global configuration

If you to define a service account globally, we suggest creating a [preset](/docs/core/scheduling-presets/).
If you are using Polyaxon Cloud or Polyaxon EE, you can add the service account name to the default organization's preset or the default project's preset.
