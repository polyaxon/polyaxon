---
title: "What is a control plane?"
meta_title: "What is a control plane? - FAQ"
meta_description: "The control plane hosts the software’s business logic and handles insensitive metadata."
featured: false
custom_excerpt: "The control plane hosts the software’s business logic and handles insensitive metadata."
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

The control plane hosts the software’s business logic and handles insensitive metadata.

It provides a managed API, metadata, scheduling, orchestration, ...

It communicates securely with Polyaxon Agent (data plane) and delegates sensitive operations (such as processing, job running, services, resolving secrets, storing or deleting data) to it.
