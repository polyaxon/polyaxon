---
title: "SSO with Github"
meta_description: "How to use github to manage users authentication on Polyaxon."
custom_excerpt: "You can easily integrate github to manage users authentication on Polyaxon."
image: "../../content/images/integrations/github.png"
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

You can GitHub to manage your organization’s entire membership.

## Register a GitHub application

You need to register a [new application](https://github.com/settings/applications/new) on github.

![github-integration1](../../content/images/integrations/sso/github.png)

You should provide a callback URL: [Domain/IP]/oauth/github

## Update your deployment config file

Use your client id and secret token to update your deployment config file.

```yaml
auth:
  github:
    enabled: true
    clientId:
    clientSecret:
```
