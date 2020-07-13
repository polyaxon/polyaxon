---
title: "Repos on Bitbucket"
meta_title: "Bitbucket"
meta_description: "How to use code from Bitbucket repositories on Polyaxon. You can use code from your Bitbucket repositories directly in Polyaxon projects without having to check them out on your local machine first."
custom_excerpt: "Bitbucket is Git repository management solution designed for professional teams. It gives you a central place to manage git repositories, collaborate on your source code and guide you through the development flow."
image: "../../content/images/integrations/bitbucket.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - scm
featured: false
popularity: 0
visibility: public
status: published
---

You can use code from your Bitbucket repositories directly in Polyaxon projects without having to check them out on your local machine first.

## Overview

Polyaxon supports repos hosted on Bitbucket (cloud and on-premise). 
You can use code from your Bitbucket repositories directly in Polyaxon projects without 
having to check them out on your local machine first. 

N.B. Polyaxon supports public and private Bitbucket repos, you don't need to have a Bitbucket account
to use code from public Bitbucket repositories.

## Access token

Bitbucket allows to create [app passwords](https://confluence.atlassian.com/bitbucket/app-passwords-828781300.html), 
you can also create a user `polyaxon` with read-only access to your organization repos, and use the username/password. 

## Create a secret

```yaml
kubectl -n polyaxon create secret generic bitbucket-connection-1 --from-literal=POLYAXON_GIT_CREDENTIALS="username:password"
```

## Add the repos you want to use to the connections catalog

```yaml
connections:
  - name: repo1
    kind: git
    schema:
      url: https://bitbucket.com/org/repo1
    secret:
      name: "bitbucket-connection-1"
  - name: repo2
    kind: git
    schema:
      url: https://bitbucket.com/org/repo2
    secret:
      name: "bitbucket-connection-1"
  - name: repo3
    kind: git
    schema:
      url: https://bitbucket.com/org/repo3
    secret:
      name: "other-connection"
```
