---
title: "Can I easily transition from self-hosted to Cloud or vice-versa?"
meta_title: "Can I easily transition from self-hosted to Cloud or vice-versa? - FAQ"
meta_description: "Yes, absolutely. You own your data, models, code, and artifacts whether you are using Polyaxon CE, Polyaxon Cloud, or Polyaxon EE."
featured: false
custom_excerpt: "Yes, absolutely. You own your data, models, code, and artifacts whether you are using Polyaxon CE, Polyaxon Cloud, or Polyaxon EE."
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
  - billing
---

Yes, absolutely. You own your data, models, code, and artifacts whether you are using Polyaxon CE, Polyaxon Cloud, or Polyaxon EE.

The difference between Polyaxon Cloud and Polyaxon EE is the control plane. In both cases, the workload, data, logs, metrics, models, artifacts, and all sensitive secrets and config-maps are managed by a Polyaxon Agent running on a different cluster/namespace.

In Polyaxon Cloud we manage the control plane, in Polyaxon EE the customer manages the control plane, in both cases the customer manages the Agent deployments (data plane).

We designed our control plane to meet the strict standards and to allow users to achieve several use-cases: data locality, federated training, federated job scheduling, support for custom networking on each Agent, namespacing and isolation, multi-cluster scaling options ...
