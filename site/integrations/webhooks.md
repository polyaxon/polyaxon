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
  - notifications
featured: false
popularity: 0
visibility: public
status: published
---

Notify a custom API when an experiment, a job, or a service is finished to extend your internal systems.

## Update your webhook settings

To send generic webhooks, you just need to set the urls that you want to send webhooks to and the http methods to use:

```yaml
notificationConnections:
  - name: service1
    kind: webhook
    configMap:
      name: "my-webhook-config"
  - name: service2
    kind: webhook
    secret:
      name: "service-with-url-token"
```
