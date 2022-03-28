---
title: "Introduction to Building Containers with Polyaxon"
sub_link: "builds"
meta_title: "Building Containers with Polyaxon - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Building Containers with Polyaxon - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
is_index: true
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

## Deploying with a registry connection

In order to build containers in-cluster with Polyaxon, you need to update your deployment with a [registry connection](/docs/setup/connections/registry/).

Polyaxon provides several options to connecting and configuring a docker registry. 
Similar to the options provided in the [integrations docs](/integrations/registries/), you can set any registry of your choice if not mentioned.

After configuring a valid registry connection, you can upgrade your deployment or sync your agent's connections:
