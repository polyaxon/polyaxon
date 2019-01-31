---
title: "SSO with Bitbucket"
meta_description: "How to use github to manage users authentication on Polyaxon."
custom_excerpt: "You can easily integrate github to manage users authentication on Polyaxon."
image: "../../content/images/integrations/bitbucket.png"
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

## Register a Bitbucket application

You need to register a [new application](https://confluence.atlassian.com/bitbucket/oauth-on-bitbucket-cloud-238027431.html) on Bitbucket.

![bitbucket-integration1](../../content/images/integrations/sso/bitbucket.png)

You should provide a callback URL: [Domain/IP]/oauth/bitbucket

## Update your deployment config file

Use your client id and secret token to update your deployment config file.

```yaml
auth:
  bitbucket:
    enabled: true
    clientId:
    clientSecret:
```
