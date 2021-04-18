---
title: "Should I deploy Polyaxon with Role Based Access Control (RBAC)?"
meta_title: "Should I deploy Polyaxon with Role Based Access Control (RBAC)? - FAQ"
meta_description: "Polyaxon ships with an RBAC enabled by default."
featured: true
custom_excerpt: "Polyaxon can natively work with RBAC enabled clusters and ships with an RBAC enabled by default."
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

Kubernetes supports, and often requires, using [Role Based Access Control (RBAC)](https://kubernetes.io/docs/admin/authorization/rbac/)
to secure which pods/users can perform what kinds of actions on the cluster.
RBAC rules can be set to provide users with minimal necessary access based on their administrative needs.

It is critical to understand that if RBAC is disabled,
all pods are given root equivalent permission on the Kubernetes cluster and all the nodes in it.
This opens up very bad vulnerabilities for your security.

Polyaxon helm chart can natively work with RBAC enabled clusters, and it's enabled by default.
To provide sensible security defaults, we ship appropriate minimal RBAC rules for the various components we use.
We highly recommend using these minimal or more restrictive RBAC rules.

If you want to disable the RBAC rules, for whatever reason, you can do so with the following snippet in your config.yaml:

```yaml
rbac:
   enabled: false
```

> We strongly discourage disabling the RBAC rules and remind you that this action will open up security vulnerabilities.
