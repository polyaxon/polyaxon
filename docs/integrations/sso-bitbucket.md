---
title: "SSO with Bitbucket"
meta_title: "Bitbucket"
meta_description: "How to use github to manage users authentication on Polyaxon. You can easily integrate github to manage users authentication on Polyaxon."
custom_excerpt: "Bitbucket is Git repository management solution designed for professional teams. It gives you a central place to manage git repositories, collaborate on your source code and guide you through the development flow."
image: "../../content/images/integrations/bitbucket.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - sso
featured: false
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
