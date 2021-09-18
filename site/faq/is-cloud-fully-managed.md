---
title: "Does Polyaxon Cloud provide a fully managed solution?"
meta_title: "Does Polyaxon Cloud provide a fully managed solution? - FAQ"
meta_description: "No, Polyaxon Cloud is not a fully managed solution."
featured: false
custom_excerpt: "No, Polyaxon Cloud is not a fully managed solution."
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

No, Polyaxon Cloud is not a fully managed solution.

Polyaxon Cloud is designed to deliver a fully managed control plane (API, metadata, scheduling, orchestration, ...) while allowing users to keep sensitive or private data on-premise or on their cloud accounts.

Polyaxon Cloud does not receive or run users’ code, it does not access their data, artifacts, or logs, and it does not alter their networking policies.

We have an abstraction called Polyaxon Agent that runs on any Kubernetes cluster, and communicates securely with our control plane.
