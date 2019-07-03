---
title: "Customize Service accounts"
sub_link: "custom-service-accounts"
meta_title: "Customize service accounts in Polyaxon - Configuration"
meta_description: "The following sections will describe how to customize the service accounts for your experiments/jobs/builds/notebooks/tensorboards."
tags:
    - configuration
    - polyaxon
    - kubernetes
    - environment
    - scheduling
    - orchestration
sidebar: "configuration"
---

<blockquote class="warning">This configuration is only available for Polyaxon deployed on Kubernetes clusters.</blockquote>

Polyaxon schedules all the pods for experiments/jobs/builds/tensorboards/notebooks with a service account `release-workers-serviceaccount` which comes with the Polyaxon deployment.

This service accounts defines a minimum requirements that our init containers and sidecars need to interact with some of the Kubernetes APIs.

Usually the default configuration works for most the use cases, but some times the amount of access 
which an experiment or a job needs is dependent on what it tries to do. 

With the introduction of Polyflow, users will need to perform complex workflow, for example, a workflow might need to deploy a resource, 
in this case the workflow's service account will require 'create' privileges on that resource. 

Starting with v0.5, Polyaxon will allow to override the default service account.   

In order for the custom service account to function correctly within Polyaxon, we recommend a bare minimum:

```yaml
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "watch", "list"]
  - apiGroups: ["metrics.k8s.io"]
    resources: ["pods", "nodes", "apis"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["", "*"]
    resources: ["events", "pods/status", "pods/log"]
    verbs: ["watch", "get", "list"]
```

## Define a default custom service account per primitive

You can create and override the default service account per kind, i.e. set a default service account for experiment, jobs, notebooks, builds, notebooks, tensorboards.

After defining a service account you can  visit the settings page, and under scheduling you can set the new service account to be used when scheduling resources for that kind.

## Define a customer service account per run

The Polyaxonfile specification's new environment allows to set a `service_account` that should be used for that run. 
For example if a user need to schedule an experiment with a custom service account:

```yaml
version: 1
kind: experiment
environment:
  service_account: my-service-account
...
```

This will tell Polyaxon to use this service account instead of the default service account.
