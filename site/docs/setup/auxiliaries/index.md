---
title: "Auxiliary Containers"
title_link: "Polyaxon's Auxiliary Containers"
sub_link: "auxiliaries"
is_index: true
meta_title: "Polyaxon's auxiliary containers provide utilities to initialize and watch users' workload."
meta_description: "Polyaxon's auxiliary containers provide utilities to initialize and watch users' workload."
tags:
  - setup
  - kubernetes
  - install
sidebar: "setup"
---

If you are here, we assume that you are about to deploy or upgrade Polyaxon CE or Polyaxon Agent.

## Overview

![polyaxonfile operation](../../../../content/images/references/specification/operation.png)

For each operation executed by a user, Polyaxon will inject:
 * init containers: containers that run before the main container containing the user's logic. For more details, see the [init specification section](/docs/core/specification/sidecars/).
 * sidecars: specialized containers that run as sidecars to the main container. For more details, see the [sidecars specification section](/docs/core/specification/sidecars/)

Polyaxon by default injects its own sidecar and init containers, these auxiliary containers act as helpers to facilitate several functionalities
and ensure that the user's workload has access to the required environment.

## Customization

In order to customize Polyaxon's init and sidecar container, you can update your deployment config with:

 * [A sidecar Section](/docs/setup/auxiliaries/sidecar/)
 * [An init Section](/docs/setup/auxiliaries/init/)
