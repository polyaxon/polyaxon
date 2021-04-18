---
title: "Why does polyaxon expose many labels on Kubernetes resources?"
meta_title: "Why does polyaxon expose many labels on Kubernetes resources, such as pods, deployments, services? - FAQ"
meta_description: "Polyaxon schedule every Kubernetes resource with several labels based on the common-labels prescribed by Kubernetes."
featured: true
custom_excerpt: "Polyaxon follows Kubernetes conventions for scheduling resources with Recommended Labels."
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

Kubernetes recommends a set of labels to describe resources, called Recommended Labels.

Several tools allow to visualize and manage Kubernetes objects other than kubectl and the dashboard.
A common set of labels allows tools to work interoperably, describing objects in a common manner that all tools can understand.

Polyaxon takes full advantage of using these labels, and schedules every resource object with a set of labels based on the [Kubernetes Recommended Labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/#labels).
