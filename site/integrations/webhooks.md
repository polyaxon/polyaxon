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

## Setting up a webhook

Configuring webhooks can be done through the polyaxonfile, or via a preset.
The only required fields to set up a new webhook are a trigger event and a target URL to notify.
This target URL is your application URL,
the endpoint where the POST request will be sent.
Of course, this URL must be reachable from the Internet.

If the server responds with 2xx HTTP response,
the delivery is considered successful.
Anything else is considered a failure of some kind,
and anything returned in the body of the response will be discarded.

## Update your webhook settings

To send generic webhooks, you just need to set the urls that you want to send webhooks to and the http methods to use:

```yaml
connections:
  - name: service1
    kind: webhook
    configMap:
      name: "my-webhook-config"
  - name: service2
    kind: webhook
    secret:
      name: "service-with-url-token"
```
