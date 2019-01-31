---
title: "SSO with GitLab"
meta_description: "How to use github to manage users authentication on Polyaxon."
custom_excerpt: "You can easily integrate github to manage users authentication on Polyaxon."
image: "../../content/images/integrations/gitlab.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - sso
featured: true
visibility: public
status: published
---

## Overview

You can GitLab to manage your organization’s entire membership.

## Register a GitLab application

You need to register a [new application](https://docs.gitlab.com/ce/integration/oauth_provider.html) on GitLab.

![gitlab-integration1](../../content/images/integrations/sso/gitlab.png)

You should provide a callback URL: [Domain/IP]/oauth/gitlab

## Update your deployment config file

Use your client id and secret token to update your deployment config file.

```yaml
auth:
  gitlab:
    enabled: true
    clientId:
    clientSecret:
```

If you have an on-premise Gitlab installation you can additionally provide your Gitlab url:

```yaml
auth:
  gitlab:
    enabled: true
    clientId:
    clientSecret:
    url: privateUrl
```
