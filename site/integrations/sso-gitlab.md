---
title: "SSO with GitLab"
meta_title: "SSO with GitLab"
meta_description: "How to use github to manage users authentication on Polyaxon. You can easily integrate github to manage users authentication on Polyaxon."
custom_excerpt: "GitLab is a single application for the entire software development lifecycle. From project planning and source code management to CI/CD, monitoring, and security."
image: "../../content/images/integrations/gitlab.png"
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

You can use GitLab to manage your organization’s entire membership.

## Register a GitLab application

You need to register a [new application](https://docs.gitlab.com/ce/integration/oauth_provider.html) on GitLab.

![gitlab-integration1](../../content/images/integrations/sso/gitlab.png)

You should provide a callback URL: `[Domain/IP]/sso/gitlab`

## Update your deployment config file

Use your client id and secret token to update your deployment config file.

```yaml
externalServices:
    auth:
      gitlab:
        enabled: true
        options: {client_id: "#####", client_secret: "#####"}
```

If you have an on-premise Gitlab installation you can additionally provide your Gitlab url:

```yaml
externalServices:
    auth:
      gitlab:
        enabled: true
        options: {client_id: "#####", client_secret: "#####", url: "privateUrl"}
```

