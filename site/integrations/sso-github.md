---
title: "SSO with Github"
meta_title: "Github"
meta_description: "How to use github to manage users authentication on Polyaxon. You can easily integrate github to manage users authentication on Polyaxon."
custom_excerpt: "GitHub is an online service for software development projects that use the Git revision control system."
image: "../../content/images/integrations/github.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - sso
featured: false
popularity: 0
visibility: public
status: EE
---

You can GitHub to manage your organization’s entire membership.

## Register a GitHub application

You need to register a [new application](https://github.com/settings/applications/new) on github.

![github-integration1](../../content/images/integrations/sso/github.png)

You should provide a callback URL: [Domain/IP]/oauth/github

## Update Github configuration on the settings page

You can now use your client id and secret token to set auth with Github. In Polyaxon's dashboard on the settings page under `Auth`, you can set the values for `Github`.

![github-settings](../../content/images/integrations/sso/github-settings.png)
