---
title: "Operation failed resource not found?"
meta_title: "Operation failed resource not found? - FAQ"
meta_description: "Please make sure that Polyaxon Operation CRD and Polyaxon Operator are installed in the namespace."
featured: false
custom_excerpt: "Please make sure that Polyaxon Operation CRD and Polyaxon Operator are installed in the namespace."
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
  - api
---

Please make sure that Polyaxon Operation CRD is installed in the namespace.

Please check that the operator is enabled in your Polyaxon CE or Polyaxon Agent deployment

If both the CRD and the operator are deployed and are running, you won't see this error:

```bash
kubernetes.client.rest.ApiException: (404)
```
