---
title: "What is the max number of parallel executions I can do at the same time?"
meta_title: "What is the max number of parallel executions I can do at the same time? - FAQ"
meta_description: "Parallelism and concurrency management depends on your distribution and it's configurable per deployment for the commercial offering."
featured: false
custom_excerpt: "Parallelism and concurrency management depends on your distribution and it's configurable per deployment for the commercial offering."
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
  - deployment
  - kubernetes
---

Parallelism and concurrency management depends on your distribution.

 * In Polyaxon CE, there's no concurrency management, you can submit as many operations as you want, you can scale Polyaxon to manage and monitor the executions.

 * In Polyaxon commercial offerings each Agent can manage multiple queues. Each queue has a configurable maximum concurrency and priority.
