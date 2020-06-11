---
title: "Install Polyaxon Agent on Kubernetes"
title_link: "Install Polyaxon Agent on Kubernetes"
sub_link: "agent"
is_index: true
meta_title: "How to install Polyaxon Agent on Kubernetes"
meta_description: "This is a guide to assist you through the process of setting up a Polyaxon Agent deployment using Kubernetes."
tags:
    - setup
    - kubernetes
    - install
sidebar: "setup"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

If you are here, it means that you access to a Polyaxon EE Control Plane or Polyaxon Cloud.

## Create a namespace for the agent

Agents are deployed and use a namespace to run operations
independently of other applications running on your cluster.

```bash
$ kubectl create namespace polyaxon

namespace "polyaxon" created
```

If you would like to use a different value, you must keep im mind to update the `namespace` value in your config.

## Configuration

This section will help you create a configuration file to deploy an agent.
Polyaxon Agent ships with [default values](/docs/setup/agent/reference/), however and depending on your use case
you might need to override some of these values.
To do so, you need to create a configuration file and we recommend to save it somewhere safe so that you can reuse it in the future.

Create a config file `config.yaml` or `polyaxon_config.yaml`,
and set up all information you want to override in the default config.
