---
title: "Webhooks"
meta_title: "Webhooks"
meta_description: "How to create custom API and webhook based integrations for the Polyaxon."
custom_excerpt: "To send generic webhooks, you just need to set the urls that you want to send webhooks to and the http methods to use."
image: "../../content/images/integrations/webhook.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - notification
featured: true
visibility: public
status: published
---

Notify a custom API when an experiment, a job, or a build is finished to extend your internal systems.

## Update your webhook settings

To send generic webhooks, you just need to set the urls that you want to send webhooks to and the http methods to use, 
under settings integrations, update `INTEGRATIONS_WEBHOOKS:GENERIC`:

```yaml
- url: url1
- url: url2
  method: post
- url: url2
  method: get  # N.B. This is just for illustration, get method is not recommended
```
