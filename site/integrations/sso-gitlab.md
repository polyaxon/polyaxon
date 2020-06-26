---
title: "SSO with GitLab"
meta_title: "GitLab"
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

You should provide a callback URL: [Domain/IP]/oauth/gitlab

## Update GitLab configuration on the settings page

You can now use your client id and secret token to set auth with GitLab. In Polyaxon's dashboard on the settings page under `Auth`, you can set the values for `GitLab`.

![gitlab-settings](../../content/images/integrations/sso/gitlab-settings.png)

> N.B. The Gitlab Url is only required if you have an on-premise Gitlab installation.
