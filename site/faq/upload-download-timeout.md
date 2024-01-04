---
title: "Uploading and downloading files on Polyaxon times-out with GKE ingress?"
meta_title: "Uploading and downloading files on Polyaxon times-out? - FAQ"
meta_description: "Please make sure to update the default timeout value from 30s to 600s."
featured: false
custom_excerpt: "Please make sure to update the default timeout value from 30s to 600s."
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

If you upload large files or pulling large models and you are using GKE ingress, you may experience timeouts.

## Example

Running a pull command on a large model:

```bash
polyaxon models pull -ver ${MODEL_VERSION} --project ${POLYAXON_MODEL_REPOSITORY} --path .
```

Might result in the following error:

```bash
#12 37.58 Writing contents: ━━━╸      0.5/1.2   17.7 MB/s  44% eta 0:00:39 elapsed 0:00:30
#12 37.58                             GB
#12 37.59 Error: Error connecting to Polyaxon server on `https://HOST/streams/v1/polyaxon/ORG/PROJECT/runs/ggfgg4335716440d858f6499edc4139f/artifacts`.
#12 37.59 An Error `("Connection broken: InvalidChunkLength(got length b'', 0 bytes read)", InvalidChunkLength(got length b'', 0 bytes read))` occurred.
#12 37.59 Check your host and ports configuration and your internet connection.
```
## Update timeout

On your google cloud console, go to `Network services` > `Load balancing` > `Backend services` > `polyaxon-ingress-backend-service` > `Edit Backend`:

![gke-ingress](../../content/images/faq/gke-ingress.png)

and update the default timeout value from 30s to 600s.
